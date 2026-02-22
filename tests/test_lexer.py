import pytest

from set_algebra_solver.lexer import tokenize
from set_algebra_solver.tokens import (
    TT_COMPLEMENT,
    TT_DIFFERENCE,
    TT_EOF,
    TT_IDENTIFIER,
    TT_INTERSECTION,
    TT_LPAREN,
    TT_NUMBER,
    TT_RPAREN,
    TT_UNION,
)


def test_tokenize_valid_expression():
    tokens = tokenize("A ∩ (B ∪ 12) - C'")
    token_types = [token.type for token in tokens]

    assert token_types == [
        TT_IDENTIFIER,
        TT_INTERSECTION,
        TT_LPAREN,
        TT_IDENTIFIER,
        TT_UNION,
        TT_NUMBER,
        TT_RPAREN,
        TT_DIFFERENCE,
        TT_IDENTIFIER,
        TT_COMPLEMENT,
        TT_EOF,
    ]


def test_tokenize_invalid_character():
    with pytest.raises(SyntaxError, match="Unexpected character"):
        tokenize("A + B")
