from aoc_2022.utils.day_handler import DayInterface
from aoc_2022.utils.transforms import DataTransforms
import pytest

test_input = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""


@pytest.fixture
def input():
    return test_input


def solve_day(input: str) -> int:
    ...


def test_day_4_part_1(input: str):
    assert 2 == solve_day(input)


if __name__ == "__main__":
    real_input = DayInterface(4).get_day()
    print(real_input)
