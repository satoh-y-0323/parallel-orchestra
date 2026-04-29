import pytest

from src.multiplication import multiply


@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 6),
    (0, 5, 0),
    (5, 0, 0),
    (-2, 3, -6),
    (-2, -3, 6),
    (1, 1, 1),
    (100, 200, 20000),
])
def test_multiply_returns_product(a: int, b: int, expected: int) -> None:
    # Arrange / Act / Assert
    assert multiply(a, b) == expected


def test_multiply_with_floats() -> None:
    assert multiply(0.1, 3.0) == pytest.approx(0.3)
