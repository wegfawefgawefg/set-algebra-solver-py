import itertools
from collections.abc import Mapping

REL_OPTIONS = ("equal", "A_subset_B", "B_subset_A", "disjoint", "overlap")


def satisfies_relation(a: set, b: set, relation: str) -> bool:
    if relation == "equal":
        return a == b
    if relation == "A_subset_B":
        return a.issubset(b) and a != b
    if relation == "B_subset_A":
        return b.issubset(a) and a != b
    if relation == "disjoint":
        return a.isdisjoint(b)
    if relation == "overlap":
        return bool(a.intersection(b)) and not (a.issubset(b) or b.issubset(a))
    return False


def check_assignment(assignment: Mapping[str, set], rel_table: Mapping[tuple[str, str], str]) -> bool:
    return all(satisfies_relation(assignment[id1], assignment[id2], rel) for (id1, id2), rel in rel_table.items())


def partial_check(assignment: Mapping[str, set], rel_table: Mapping[tuple[str, str], str]) -> bool:
    for (id1, id2), rel in rel_table.items():
        if id1 in assignment and id2 in assignment:
            if not satisfies_relation(assignment[id1], assignment[id2], rel):
                return False
    return True


def powerset(source: set) -> list[set]:
    items = sorted(source)
    result: list[set] = []
    for size in range(len(items) + 1):
        for combo in itertools.combinations(items, size):
            result.append(set(combo))
    return result


def generate_assignment(
    identifiers: list[str] | set[str],
    rel_table: Mapping[tuple[str, str], str],
    candidate_universe: set,
) -> dict[str, set] | None:
    candidate_sets = sorted(
        powerset(candidate_universe),
        key=lambda current_set: (len(current_set), tuple(sorted(current_set))),
    )
    ordered_ids = list(identifiers)

    def backtrack(index: int, current_assignment: dict[str, set]) -> dict[str, set] | None:
        if index == len(ordered_ids):
            return current_assignment.copy() if check_assignment(current_assignment, rel_table) else None

        current_id = ordered_ids[index]
        for candidate in candidate_sets:
            current_assignment[current_id] = candidate
            if partial_check(current_assignment, rel_table):
                result = backtrack(index + 1, current_assignment)
                if result is not None:
                    return result

        current_assignment.pop(current_id, None)
        return None

    return backtrack(0, {})
