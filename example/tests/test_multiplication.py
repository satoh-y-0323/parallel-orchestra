import pytest
from example.src.multiplication import multiply


def test_multiply_two_integers() -> None:
    assert multiply(3, 4) == 12


def test_multiply_by_zero() -> None:
    assert multiply(5, 0) == 0


def test_multiply_negative_numbers() -> None:
    assert multiply(-2, 3) == -6


def test_multiply_floats() -> None:
    assert multiply(1.5, 2.0) == pytest.approx(3.0)


def test_multiply_int_and_float() -> None:
    assert multiply(2, 2.5) == pytest.approx(5.0)
