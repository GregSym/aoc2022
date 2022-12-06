import collections
from aoc_2022.utils.day_handler import DayInterface
from aoc_2022.utils.transforms import DataTransforms
import pytest

test_input = """mjqjpqmgbljsphdztnvjfqwrcgsmlb"""


@pytest.fixture
def input():
    return test_input


def solve_day(input: str) -> int:
    info = input  # no manipulation necessary
    code_window = collections.deque([], 4)
    for i, c in enumerate(info):
        code_window.append(c)
        if len(code_window) == len(set(code_window)) and len(code_window) == 4:
            return i + 1
    return 0


def test_day_6_part_1(input: str) -> None:
    assert 7 == solve_day(input)
    assert 5 == solve_day("bvwbjplbgvbhsrlpgdmjqwftvncz")


if __name__ == "__main__":
    real_input = DayInterface(6).get_day()
    print(solve_day(real_input))
