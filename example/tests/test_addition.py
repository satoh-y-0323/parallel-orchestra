import pytest

from src.addition import add


@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
    (-3, -4, -7),
    (100, 200, 300),
])
def test_add_returns_sum(a: int, b: int, expected: int) -> None:
    # Arrange / Act / Assert
    assert add(a, b) == expected


def test_add_with_floats() -> None:
    assert add(0.1, 0.2) == pytest.approx(0.3)
