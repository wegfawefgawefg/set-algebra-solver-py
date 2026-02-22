import pytest

from set_algebra_solver.identity import (
    evaluate_identity_with_relations,
    extract_identifiers,
    parse_equality_expression,
)
from set_algebra_solver.parser import parse_expression


def test_extract_identifiers_from_expression_tree():
    ast = parse_expression("(A ∩ B) ∪ C")

    assert extract_identifiers(ast) == {"A", "B", "C"}


def test_parse_equality_expression_success():
    lhs, rhs = parse_equality_expression("A ∪ B = B ∪ A")

    assert extract_identifiers(lhs) == {"A", "B"}
    assert extract_identifiers(rhs) == {"A", "B"}


@pytest.mark.parametrize(
    "expr,error_pattern",
    [
        ("A ∪ B", "exactly one '='"),
        ("A = B = C", "exactly one '='"),
        ("= B", "non-empty"),
        ("A =", "non-empty"),
    ],
)
def test_parse_equality_expression_invalid(expr, error_pattern):
    with pytest.raises(SyntaxError, match=error_pattern):
        parse_equality_expression(expr)


def test_commutative_identity_holds_for_all_satisfiable_outcomes():
    result = evaluate_identity_with_relations("A ∪ B = B ∪ A", {1, 2, 3})

    assert result.identifiers == ["A", "B"]
    assert len(result.outcomes) == 5

    satisfiable = [outcome for outcome in result.outcomes if outcome.assignment is not None]
    assert satisfiable
    assert all(outcome.holds is True for outcome in satisfiable)


def test_non_identity_has_counterexample():
    result = evaluate_identity_with_relations("A - B = B - A", {1, 2, 3})

    satisfiable = [outcome for outcome in result.outcomes if outcome.assignment is not None]
    assert satisfiable
    assert any(outcome.holds is False for outcome in satisfiable)
