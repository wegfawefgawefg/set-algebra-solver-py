from set_algebra_solver.relations import (
    check_assignment,
    generate_assignment,
    partial_check,
    powerset,
    satisfies_relation,
)


def test_satisfies_relation_variants():
    a = {1}
    b = {1, 2}

    assert satisfies_relation(a, b, "A_subset_B")
    assert satisfies_relation(b, a, "B_subset_A")
    assert satisfies_relation({1}, {1}, "equal")
    assert satisfies_relation({1}, {2}, "disjoint")
    assert satisfies_relation({1, 2}, {2, 3}, "overlap")
    assert not satisfies_relation({1}, {2}, "unknown")


def test_powerset_size():
    assert len(powerset({1, 2, 3})) == 8


def test_generate_assignment_satisfiable_relation():
    assignment = generate_assignment(
        identifiers=["A", "B"],
        rel_table={("A", "B"): "A_subset_B"},
        candidate_universe={1, 2},
    )

    assert assignment is not None
    assert assignment["A"].issubset(assignment["B"])
    assert assignment["A"] != assignment["B"]


def test_generate_assignment_unsatisfiable_with_small_universe():
    assignment = generate_assignment(
        identifiers=["A", "B"],
        rel_table={("A", "B"): "overlap"},
        candidate_universe={1},
    )

    assert assignment is None


def test_check_and_partial_check():
    rel_table = {("A", "B"): "disjoint"}
    good_assignment = {"A": {1}, "B": {2}}
    partial_assignment = {"A": {1}}
    bad_assignment = {"A": {1}, "B": {1}}

    assert partial_check(partial_assignment, rel_table)
    assert check_assignment(good_assignment, rel_table)
    assert not partial_check(bad_assignment, rel_table)
