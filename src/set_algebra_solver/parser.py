from .ast_nodes import BinOp, Complement, Identifier, SetLiteral
from .lexer import tokenize
from .tokens import (
    TT_COMMA,
    TT_COMPLEMENT,
    TT_DIFFERENCE,
    TT_EOF,
    TT_IDENTIFIER,
    TT_INTERSECTION,
    TT_LBRACE,
    TT_LPAREN,
    TT_NUMBER,
    TT_RBRACE,
    TT_RPAREN,
    TT_UNION,
    Token,
)


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos]

    def eat(self, token_type: str) -> Token:
        if self.current_token.type != token_type:
            raise SyntaxError(f"Expected {token_type}, got {self.current_token.type}")

        token = self.current_token
        self.pos += 1
        self.current_token = self.tokens[self.pos]
        return token

    def parse(self):
        node = self.expr()
        if self.current_token.type != TT_EOF:
            raise SyntaxError(f"Unexpected token: {self.current_token}")
        return node

    def expr(self):
        node = self.term()
        while self.current_token.type in (TT_UNION, TT_INTERSECTION, TT_DIFFERENCE):
            op = self.current_token.type
            self.eat(op)
            right = self.term()
            node = BinOp(node, op, right)
        return node

    def term(self):
        node = self.primary()
        while self.current_token.type == TT_COMPLEMENT:
            self.eat(TT_COMPLEMENT)
            node = Complement(node)
        return node

    def primary(self):
        token = self.current_token

        if token.type == TT_IDENTIFIER:
            self.eat(TT_IDENTIFIER)
            return Identifier(token.value or "")

        if token.type == TT_NUMBER:
            self.eat(TT_NUMBER)
            return int(token.value or "0")

        if token.type == TT_LBRACE:
            return self.set_literal()

        if token.type == TT_LPAREN:
            self.eat(TT_LPAREN)
            node = self.expr()
            self.eat(TT_RPAREN)
            return node

        raise SyntaxError(f"Unexpected token: {token}")

    def set_literal(self):
        elements: list = []
        self.eat(TT_LBRACE)

        if self.current_token.type == TT_RBRACE:
            self.eat(TT_RBRACE)
            return SetLiteral(elements)

        while True:
            elements.append(self.term())

            if self.current_token.type == TT_COMMA:
                self.eat(TT_COMMA)
                if self.current_token.type == TT_RBRACE:
                    raise SyntaxError("Trailing comma is not allowed in set literals")
                continue

            if self.current_token.type == TT_RBRACE:
                self.eat(TT_RBRACE)
                return SetLiteral(elements)

            raise SyntaxError(f"Expected ',' or '}}', got {self.current_token.type}")


def parse_expression(text: str):
    return Parser(tokenize(text)).parse()
