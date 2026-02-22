import pytest

from set_algebra_solver.evaluator import Evaluator
from set_algebra_solver.parser import parse_expression


def test_evaluate_basic_union_intersection_difference():
    evaluator = Evaluator(context={"A": {1, 2}, "B": {2, 3}})

    assert evaluator.eval(parse_expression("A ∪ B")) == {1, 2, 3}
    assert evaluator.eval(parse_expression("A ∩ B")) == {2}
    assert evaluator.eval(parse_expression("A - B")) == {1}


def test_evaluate_set_literal():
    evaluator = Evaluator()

    assert evaluator.eval(parse_expression("{1,2,3}")) == {1, 2, 3}


def test_evaluate_undefined_identifier_raises():
    evaluator = Evaluator(context={})

    with pytest.raises(ValueError, match="Undefined set"):
        evaluator.eval(parse_expression("A"))


def test_evaluate_complement_not_implemented():
    evaluator = Evaluator(context={"A": {1}})

    with pytest.raises(NotImplementedError, match="Complement evaluation"):
        evaluator.eval(parse_expression("A'"))


def test_evaluate_nested_set_values_are_rejected():
    evaluator = Evaluator(context={"A": {1}})

    with pytest.raises(ValueError, match="Nested set values"):
        evaluator.eval(parse_expression("{A}"))
