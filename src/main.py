import re, itertools

# --- Tokenization Constants ---
TT_IDENTIFIER    = 'IDENTIFIER'
TT_NUMBER        = 'NUMBER'
TT_LBRACE        = '{'
TT_RBRACE        = '}'
TT_LPAREN        = '('
TT_RPAREN        = ')'
TT_COMMA         = ','
TT_UNION         = 'UNION'
TT_INTERSECTION  = 'INTERSECTION'
TT_DIFFERENCE    = 'DIFFERENCE'
TT_COMPLEMENT    = 'COMPLEMENT'
TT_EOF           = 'EOF'

TOKEN_SPEC = [
    (r'\s+',              None),
    (r'\{',               TT_LBRACE),
    (r'\}',               TT_RBRACE),
    (r'\(',               TT_LPAREN),
    (r'\)',               TT_RPAREN),
    (r',',                TT_COMMA),
    (r'∪|\|',             TT_UNION),
    (r'∩|&',             TT_INTERSECTION),
    (r'-',                TT_DIFFERENCE),
    (r"'",                TT_COMPLEMENT),
    (r'\d+',              TT_NUMBER),
    (r'[A-Za-z_]\w*',     TT_IDENTIFIER),
]

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value
    def __repr__(self):
        return f'Token({self.type}, {self.value})'

def tokenize(text):
    tokens = []
    pos = 0
    while pos < len(text):
        match = None
        for pattern, token_type in TOKEN_SPEC:
            regex = re.compile(pattern)
            match = regex.match(text, pos)
            if match:
                if token_type:
                    tokens.append(Token(token_type, match.group(0)))
                break
        if not match:
            raise SyntaxError(f"Unexpected character: {text[pos]}")
        pos = match.end(0)
    tokens.append(Token(TT_EOF, None))
    return tokens

# --- AST Node Definitions ---
class ASTNode:
    pass

class Identifier(ASTNode):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f'Identifier({self.name})'

class SetLiteral(ASTNode):
    def __init__(self, elements):
        self.elements = elements  # list of AST nodes (Identifier, Number)
    def __repr__(self):
        return f'SetLiteral({self.elements})'

class BinOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op   # TT_UNION, TT_INTERSECTION, or TT_DIFFERENCE
        self.right = right
    def __repr__(self):
        return f'BinOp({self.left}, {self.op}, {self.right})'

class Complement(ASTNode):
    def __init__(self, node):
        self.node = node
    def __repr__(self):
        return f'Complement({self.node})'

# --- Parser (Recursive Descent) ---
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = tokens[self.pos]
    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.pos += 1
            self.current_token = self.tokens[self.pos]
        else:
            raise SyntaxError(f"Expected {token_type}, got {self.current_token.type}")
    def parse(self):
        return self.expr()
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
            return Identifier(token.value)
        elif token.type == TT_NUMBER:
            self.eat(TT_NUMBER)
            return int(token.value)
        elif token.type == TT_LBRACE:
            return self.set_literal()
        elif token.type == TT_LPAREN:
            self.eat(TT_LPAREN)
            node = self.expr()
            self.eat(TT_RPAREN)
            return node
        else:
            raise SyntaxError(f"Unexpected token: {token}")
    def set_literal(self):
        elements = []
        self.eat(TT_LBRACE)
        while self.current_token.type != TT_RBRACE:
            elem = self.term()
            elements.append(elem)
            if self.current_token.type == TT_COMMA:
                self.eat(TT_COMMA)
        self.eat(TT_RBRACE)
        return SetLiteral(elements)

# --- Evaluator ---
class Evaluator:
    def __init__(self, context=None):
        # context is a dict mapping identifier names to Python sets
        self.context = context if context is not None else {}
    def eval(self, node):
        if isinstance(node, Identifier):
            if node.name in self.context:
                return self.context[node.name]
            else:
                raise ValueError(f"Undefined set: {node.name}")
        elif isinstance(node, SetLiteral):
            # Assume literals are concrete (only numbers)
            result = set()
            for el in node.elements:
                val = self.eval(el) if isinstance(el, ASTNode) else el
                result.add(val)
            return result
        elif isinstance(node, BinOp):
            left_val = self.eval(node.left)
            right_val = self.eval(node.right)
            if node.op == TT_UNION:
                return left_val.union(right_val)
            elif node.op == TT_INTERSECTION:
                return left_val.intersection(right_val)
            elif node.op == TT_DIFFERENCE:
                return left_val.difference(right_val)
            else:
                raise ValueError(f"Unknown operator: {node.op}")
        elif isinstance(node, Complement):
            # For now, we do not directly evaluate complements in our identity tester.
            raise NotImplementedError("Complement evaluation not implemented in this solver")
        elif isinstance(node, int):
            return node
        else:
            raise ValueError(f"Unknown AST node: {node}")

# --- Identifier Extraction ---
def extract_identifiers(ast_node):
    ids = set()
    if isinstance(ast_node, Identifier):
        ids.add(ast_node.name)
    elif isinstance(ast_node, SetLiteral):
        for el in ast_node.elements:
            ids.update(extract_identifiers(el))
    elif isinstance(ast_node, BinOp):
        ids.update(extract_identifiers(ast_node.left))
        ids.update(extract_identifiers(ast_node.right))
    elif isinstance(ast_node, Complement):
        ids.update(extract_identifiers(ast_node.node))
    return ids

# --- Relationship Constraint Helpers ---
# We'll consider these options for each unordered pair (A, B)
REL_OPTIONS = ["equal", "A_subset_B", "B_subset_A", "disjoint", "overlap"]

def satisfies_relation(a, b, rel):
    if rel == "equal":
        return a == b
    elif rel == "A_subset_B":
        return a.issubset(b) and a != b
    elif rel == "B_subset_A":
        return b.issubset(a) and a != b
    elif rel == "disjoint":
        return a.isdisjoint(b)
    elif rel == "overlap":
        return bool(a.intersection(b)) and not (a.issubset(b) or b.issubset(a))
    else:
        return False

def check_assignment(assignment, rel_table):
    for (id1, id2), rel in rel_table.items():
        if not satisfies_relation(assignment[id1], assignment[id2], rel):
            return False
    return True

def partial_check(assignment, rel_table):
    # Only check pairs where both identifiers have been assigned
    for (id1, id2), rel in rel_table.items():
        if id1 in assignment and id2 in assignment:
            if not satisfies_relation(assignment[id1], assignment[id2], rel):
                return False
    return True

def powerset(s):
    s = list(s)
    ps = []
    for r in range(len(s)+1):
        for comb in itertools.combinations(s, r):
            ps.append(set(comb))
    return ps

def generate_assignment(identifiers, rel_table, candidate_universe):
    # Generate candidate sets from a small universe
    candidate_sets = powerset(candidate_universe)
    # Sort candidates by size (to favor minimal sets)
    candidate_sets = sorted(candidate_sets, key=lambda s: (len(s), s))
    identifiers = list(identifiers)
    
    def backtrack(index, current_assignment):
        if index == len(identifiers):
            if check_assignment(current_assignment, rel_table):
                return current_assignment.copy()
            return None
        current_id = identifiers[index]
        for candidate in candidate_sets:
            current_assignment[current_id] = candidate
            if partial_check(current_assignment, rel_table):
                result = backtrack(index+1, current_assignment)
                if result is not None:
                    return result
        if current_id in current_assignment:
            del current_assignment[current_id]
        return None
    
    return backtrack(0, {})

# --- Main Equality Testing with Relationship Tables ---
def evaluate_identity_with_relations(equality_expr, candidate_universe):
    # Split the equality expression at '=' and parse both sides
    lhs_str, rhs_str = equality_expr.split('=')
    lhs_str, rhs_str = lhs_str.strip(), rhs_str.strip()
    lhs_ast = Parser(tokenize(lhs_str)).parse()
    rhs_ast = Parser(tokenize(rhs_str)).parse()
    
    # Extract unique identifiers from both sides
    identifiers = extract_identifiers(lhs_ast).union(extract_identifiers(rhs_ast))
    identifiers = sorted(identifiers)
    print("Identifiers:", identifiers)
    
    # List all unordered pairs (for which we assign a relation)
    pairs = list(itertools.combinations(identifiers, 2))
    
    # Build all relational combinations over these pairs
    all_rel_tables = []
    for rel_combo in itertools.product(REL_OPTIONS, repeat=len(pairs)):
        rel_table = {}
        for idx, pair in enumerate(pairs):
            rel_table[pair] = rel_combo[idx]
        all_rel_tables.append(rel_table)
    
    print(f"Total relational combinations: {len(all_rel_tables)}")
    
    # For each relational table, try to generate a realized assignment and test the identity
    for rel_table in all_rel_tables:
        print("\nTesting relational table:")
        for (id1, id2), rel in rel_table.items():
            print(f"  {id1} and {id2}: {rel}")
        assignment = generate_assignment(identifiers, rel_table, candidate_universe)
        if assignment is None:
            print("  No assignment found for these relationships.")
            continue
        print("  Realized assignment:")
        for id, s in assignment.items():
            print(f"    {id} = {s}")
        evaluator = Evaluator(context=assignment)
        lhs_val = evaluator.eval(lhs_ast)
        rhs_val = evaluator.eval(rhs_ast)
        print("  LHS evaluates to:", lhs_val)
        print("  RHS evaluates to:", rhs_val)
        if lhs_val == rhs_val:
            print("  -> Identity holds under these relationships.")
        else:
            print("  -> Identity fails under these relationships.")

# --- Example Usage ---
if __name__ == "__main__":
    # Use a small candidate universe for generating realized sets.
    candidate_universe = {1, 2, 3}
    # Example equality expression.
    expr = "A ∪ B = B ∪ A"
    print("Evaluating identity:", expr)
    evaluate_identity_with_relations(expr, candidate_universe)
