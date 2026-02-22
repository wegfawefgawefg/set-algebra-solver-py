# Intent Speculation

This document captures a best-effort read of what this project appears to have been aiming for when it was first started.

## What You Were Probably Building

A bounded set-algebra explorer with two goals:

- Find concrete assignments of sets to variables (`A`, `B`, `C`, ...).
- Test whether an identity holds or fails under those assignments.

In other words: a finite model finder and counterexample generator for set identities.

## Why This Interpretation Fits

The structure of the code strongly points to search over concrete assignments rather than symbolic proving:

- Expressions are parsed into an AST.
- Identifiers are extracted from both sides of an equality.
- Pairwise relationship tables are generated (`equal`, subset directions, disjoint, overlap).
- Backtracking builds concrete assignments from a bounded universe.
- Each assignment is evaluated on both sides, then marked hold/fail.

That workflow is exactly what you would implement for “find me a witness” or “find me a counterexample.”

## Concrete Example

Expression:

`A - B = B - A`

One relation scenario:

- `A_subset_B`

A concrete assignment that satisfies that relation:

- `A = {}`
- `B = {1}`

Evaluation:

- LHS: `A - B = {}`
- RHS: `B - A = {1}`

Result: not equal, so this is a counterexample.

## What It Looks Like You Had Not Finished

- Complement evaluation (`A'`) is parsed but not evaluated yet.
- No symbolic rewrite/canonicalization system is present yet.
- No proof search over expression transforms is present yet.

This suggests your first milestone was likely concrete behavioral checking, with symbolic solving planned for later.

## Plausible Next Direction You Might Have Been Heading Toward

- Keep the current bounded counterexample engine for fast falsification.
- Add a symbolic normalization/rewrite engine for proving equalities.
- Combine both:
  - Try symbolic proof first.
  - Fall back to model finding for counterexamples.

That hybrid approach matches the current architecture well.
