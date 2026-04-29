import pytest

from example.src.addition import add


@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
    (-3, -2, -5),
    (1.5, 2.5, 4.0),
    (0.1, 0.2, pytest.approx(0.3)),
])
def test_add(a: int | float, b: int | float, expected: int | float) -> None:
    # Act
    result = add(a, b)

    # Assert
    assert result == expected
