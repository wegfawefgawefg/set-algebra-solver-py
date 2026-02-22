from dataclasses import dataclass


class ASTNode:
    """Marker base class for expression nodes."""


@dataclass(frozen=True)
class Identifier(ASTNode):
    name: str


@dataclass(frozen=True)
class SetLiteral(ASTNode):
    elements: list[ASTNode | int]


@dataclass(frozen=True)
class BinOp(ASTNode):
    left: ASTNode | int
    op: str
    right: ASTNode | int


@dataclass(frozen=True)
class Complement(ASTNode):
    node: ASTNode | int
