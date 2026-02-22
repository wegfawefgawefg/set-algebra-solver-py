# Features

## Current

- Tokenization for identifiers, integers, braces, parentheses, commas, and set operators.
- Parser for union, intersection, difference, complement postfix, grouping, and set literals.
- AST-based evaluation for union, intersection, and difference.
- Identity evaluation across pairwise relationship assumptions:
  - `equal`
  - `A_subset_B`
  - `B_subset_A`
  - `disjoint`
  - `overlap`
- Backtracking assignment generator over a finite candidate universe.
- CLI entrypoint exposed through `uv run set-algebra-solver`.

## Not Yet Implemented

- Complement evaluation against an explicit universal set.
- Algebraic simplification and canonicalization.
- Counterexample minimization and richer diagnostics.
- Performance optimizations for larger identifier sets.

## Planned Direction

- Introduce rewrite rules for set algebra identities.
- Build a normalized representation for equivalence checks.
- Explore graph search over expression transforms.
- Consider e-graph style equality saturation for scalable automated proving.
- Expose solver modes:
  - brute-force counterexample search
  - rewrite-prove mode
  - mixed strategy with fallback
