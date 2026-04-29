import pytest

from example.src.multiplication import multiply


@pytest.mark.parametrize("a,b,expected", [
    (3, 4, 12),
    (5, 0, 0),
    (0, 5, 0),
    (-2, 3, -6),
    (-2, -3, 6),
])
def test_multiply_integers(a: int, b: int, expected: int) -> None:
    # Act
    result = multiply(a, b)

    # Assert
    assert result == expected


@pytest.mark.parametrize("a,b,expected", [
    (1.5, 2.0, 3.0),
    (2, 2.5, 5.0),
    (-1.5, 2.0, -3.0),
])
def test_multiply_floats(a: float, b: float, expected: float) -> None:
    # Act
    result = multiply(a, b)

    # Assert
    assert result == pytest.approx(expected)
