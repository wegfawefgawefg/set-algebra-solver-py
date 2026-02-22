from collections.abc import Mapping

from .ast_nodes import ASTNode, BinOp, Complement, Identifier, SetLiteral
from .tokens import TT_DIFFERENCE, TT_INTERSECTION, TT_UNION


class Evaluator:
    def __init__(self, context: Mapping[str, set] | None = None):
        self.context = dict(context or {})

    def eval(self, node):
        if isinstance(node, Identifier):
            if node.name in self.context:
                return self.context[node.name]
            raise ValueError(f"Undefined set: {node.name}")

        if isinstance(node, SetLiteral):
            result = set()
            for element in node.elements:
                value = self.eval(element) if isinstance(element, ASTNode) else element
                if isinstance(value, set):
                    raise ValueError("Nested set values are not supported in set literals")
                result.add(value)
            return result

        if isinstance(node, BinOp):
            left_val = self.eval(node.left)
            right_val = self.eval(node.right)

            if node.op == TT_UNION:
                return left_val.union(right_val)
            if node.op == TT_INTERSECTION:
                return left_val.intersection(right_val)
            if node.op == TT_DIFFERENCE:
                return left_val.difference(right_val)

            raise ValueError(f"Unknown operator: {node.op}")

        if isinstance(node, Complement):
            raise NotImplementedError("Complement evaluation is not implemented")

        if isinstance(node, int):
            return node

        raise ValueError(f"Unknown AST node: {node}")
