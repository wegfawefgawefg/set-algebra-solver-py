import re

from .tokens import TOKEN_SPEC, TT_EOF, Token


_COMPILED_SPEC = [(re.compile(pattern), token_type) for pattern, token_type in TOKEN_SPEC]


def tokenize(text: str) -> list[Token]:
    tokens: list[Token] = []
    pos = 0

    while pos < len(text):
        match = None
        for regex, token_type in _COMPILED_SPEC:
            match = regex.match(text, pos)
            if match:
                if token_type is not None:
                    tokens.append(Token(token_type, match.group(0)))
                break

        if not match:
            raise SyntaxError(f"Unexpected character: {text[pos]}")

        pos = match.end(0)

    tokens.append(Token(TT_EOF, None))
    return tokens
