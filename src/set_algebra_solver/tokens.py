from dataclasses import dataclass

TT_IDENTIFIER = "IDENTIFIER"
TT_NUMBER = "NUMBER"
TT_LBRACE = "{"
TT_RBRACE = "}"
TT_LPAREN = "("
TT_RPAREN = ")"
TT_COMMA = ","
TT_UNION = "UNION"
TT_INTERSECTION = "INTERSECTION"
TT_DIFFERENCE = "DIFFERENCE"
TT_COMPLEMENT = "COMPLEMENT"
TT_EOF = "EOF"

TOKEN_SPEC = [
    (r"\s+", None),
    (r"\{", TT_LBRACE),
    (r"\}", TT_RBRACE),
    (r"\(", TT_LPAREN),
    (r"\)", TT_RPAREN),
    (r",", TT_COMMA),
    (r"∪|\|", TT_UNION),
    (r"∩|&", TT_INTERSECTION),
    (r"-", TT_DIFFERENCE),
    (r"'", TT_COMPLEMENT),
    (r"\d+", TT_NUMBER),
    (r"[A-Za-z_]\w*", TT_IDENTIFIER),
]


@dataclass(frozen=True)
class Token:
    type: str
    value: str | None
