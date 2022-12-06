import collections
from aoc_2022.utils.day_handler import DayInterface
from aoc_2022.utils.transforms import DataTransforms
import pytest

test_input = """mjqjpqmgbljsphdztnvjfqwrcgsmlb"""


@pytest.fixture
def input():
    return test_input


def solve_day(input: str, w_size: int = 4) -> int:
    info = input  # no manipulation necessary
    code_window = collections.deque([], w_size)
    for i, c in enumerate(info):
        code_window.append(c)
        if len(code_window) == len(set(code_window)) and len(code_window) == w_size:
            return i + 1
    return 0


def test_day_6_part_1(input: str) -> None:
    assert 7 == solve_day(input)
    assert 5 == solve_day("bvwbjplbgvbhsrlpgdmjqwftvncz")


def test_day_6_part_2(input: str) -> None:
    assert 19 == solve_day(input, 14)
    assert 23 == solve_day("bvwbjplbgvbhsrlpgdmjqwftvncz", 14)


if __name__ == "__main__":
    real_input = DayInterface(6).get_day()
    print(solve_day(real_input))
    test_day_6_part_1(test_input)
    test_day_6_part_2(test_input)
    DayInterface(6).submit_day(solve_day(real_input, 14), 2)
