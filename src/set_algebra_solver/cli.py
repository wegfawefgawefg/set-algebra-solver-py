import argparse

from .identity import evaluate_identity_with_relations


def parse_universe(raw_value: str) -> set[int]:
    if not raw_value.strip():
        return set()

    try:
        return {int(item.strip()) for item in raw_value.split(",")}
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Universe must be a comma-separated list of integers") from exc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Evaluate set identities across pairwise relation assumptions")
    parser.add_argument(
        "expression",
        nargs="?",
        default="A ∪ B = B ∪ A",
        help="Set identity expression using one '=' between left and right sides",
    )
    parser.add_argument(
        "--universe",
        type=parse_universe,
        default={1, 2, 3},
        help="Comma-separated integers used to generate candidate sets (default: 1,2,3)",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    result = evaluate_identity_with_relations(args.expression, args.universe)

    print(f"Expression: {result.expression}")
    print(f"Identifiers: {result.identifiers}")
    print(f"Relation tables explored: {len(result.outcomes)}")

    for outcome in result.outcomes:
        print("\nRelation table:")
        if outcome.relation_table:
            for (id1, id2), relation in outcome.relation_table.items():
                print(f"  {id1}/{id2}: {relation}")
        else:
            print("  (none)")

        if outcome.assignment is None:
            print("  No satisfying assignment found for this relation table.")
            continue

        print("  Assignment:")
        for identifier, assigned_set in outcome.assignment.items():
            print(f"    {identifier} = {assigned_set}")
        print(f"  LHS: {outcome.lhs_value}")
        print(f"  RHS: {outcome.rhs_value}")
        print(f"  Identity holds: {outcome.holds}")

    return 0
