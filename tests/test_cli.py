import argparse

import pytest

from set_algebra_solver.cli import build_parser, parse_universe


def test_parse_universe_valid_values():
    assert parse_universe("1,2,3") == {1, 2, 3}
    assert parse_universe(" 1, 2 , 3 ") == {1, 2, 3}
    assert parse_universe("") == set()


def test_parse_universe_invalid_values():
    with pytest.raises(argparse.ArgumentTypeError, match="comma-separated list of integers"):
        parse_universe("1,two,3")


def test_build_parser_defaults():
    parser = build_parser()
    parsed = parser.parse_args([])

    assert parsed.expression == "A ∪ B = B ∪ A"
    assert parsed.universe == {1, 2, 3}
