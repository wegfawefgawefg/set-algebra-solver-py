import pytest

from set_algebra_solver.ast_nodes import BinOp, Complement, Identifier, SetLiteral
from set_algebra_solver.parser import parse_expression
from set_algebra_solver.tokens import TT_UNION


def test_parse_union_expression():
    ast = parse_expression("A ∪ B")

    assert isinstance(ast, BinOp)
    assert ast.op == TT_UNION
    assert ast.left == Identifier("A")
    assert ast.right == Identifier("B")


def test_parse_empty_set_literal():
    ast = parse_expression("{}")

    assert ast == SetLiteral([])


def test_parse_set_literal_with_numbers():
    ast = parse_expression("{1, 2, 3}")

    assert ast == SetLiteral([1, 2, 3])


def test_parse_multiple_complements():
    ast = parse_expression("A''")

    assert isinstance(ast, Complement)
    assert isinstance(ast.node, Complement)
    assert ast.node.node == Identifier("A")


@pytest.mark.parametrize(
    "expression,error_pattern",
    [
        ("(A ∪ B", r"Expected \)"),
        ("A B", "Unexpected token"),
        ("{1 2}", "Expected ',' or '}'"),
        ("{1,}", "Trailing comma"),
        ("A ∪", "Unexpected token"),
    ],
)
def test_parse_invalid_expressions(expression, error_pattern):
    with pytest.raises(SyntaxError, match=error_pattern):
        parse_expression(expression)
