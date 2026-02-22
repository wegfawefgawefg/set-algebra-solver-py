import itertools
from dataclasses import dataclass

from .ast_nodes import ASTNode, BinOp, Complement, Identifier, SetLiteral
from .evaluator import Evaluator
from .parser import parse_expression
from .relations import REL_OPTIONS, generate_assignment


@dataclass(frozen=True)
class RelationOutcome:
    relation_table: dict[tuple[str, str], str]
    assignment: dict[str, set] | None
    lhs_value: set | None
    rhs_value: set | None
    holds: bool | None


@dataclass(frozen=True)
class IdentityEvaluation:
    expression: str
    identifiers: list[str]
    outcomes: list[RelationOutcome]


def extract_identifiers(ast_node) -> set[str]:
    ids: set[str] = set()

    if isinstance(ast_node, Identifier):
        ids.add(ast_node.name)
    elif isinstance(ast_node, SetLiteral):
        for element in ast_node.elements:
            ids.update(extract_identifiers(element))
    elif isinstance(ast_node, BinOp):
        ids.update(extract_identifiers(ast_node.left))
        ids.update(extract_identifiers(ast_node.right))
    elif isinstance(ast_node, Complement):
        ids.update(extract_identifiers(ast_node.node))

    return ids


def parse_equality_expression(equality_expr: str) -> tuple[ASTNode | int, ASTNode | int]:
    if equality_expr.count("=") != 1:
        raise SyntaxError("Identity expression must contain exactly one '='")

    lhs_str, rhs_str = (part.strip() for part in equality_expr.split("=", maxsplit=1))
    if not lhs_str or not rhs_str:
        raise SyntaxError("Both sides of the identity expression must be non-empty")

    return parse_expression(lhs_str), parse_expression(rhs_str)


def evaluate_identity_with_relations(equality_expr: str, candidate_universe: set) -> IdentityEvaluation:
    lhs_ast, rhs_ast = parse_equality_expression(equality_expr)

    identifiers = sorted(extract_identifiers(lhs_ast).union(extract_identifiers(rhs_ast)))
    pairs = list(itertools.combinations(identifiers, 2))

    outcomes: list[RelationOutcome] = []
    for relation_choice in itertools.product(REL_OPTIONS, repeat=len(pairs)):
        rel_table = {pair: relation_choice[idx] for idx, pair in enumerate(pairs)}
        assignment = generate_assignment(identifiers, rel_table, candidate_universe)

        if assignment is None:
            outcomes.append(
                RelationOutcome(
                    relation_table=rel_table,
                    assignment=None,
                    lhs_value=None,
                    rhs_value=None,
                    holds=None,
                )
            )
            continue

        evaluator = Evaluator(context=assignment)
        lhs_val = evaluator.eval(lhs_ast)
        rhs_val = evaluator.eval(rhs_ast)

        outcomes.append(
            RelationOutcome(
                relation_table=rel_table,
                assignment=assignment,
                lhs_value=lhs_val,
                rhs_value=rhs_val,
                holds=lhs_val == rhs_val,
            )
        )

    return IdentityEvaluation(expression=equality_expr, identifiers=identifiers, outcomes=outcomes)
