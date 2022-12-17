from aoc_2022.utils.day_handler import DayInterface
from aoc_2022.utils.transforms import DataTransforms
import pytest

test_input = """noop
addx 3
addx -5"""


@pytest.fixture
def input():
    return test_input


def solve_day(input: str) -> int:
    ...


def test_day_10_part_1(input: str) -> None:
    assert 13140 == solve_day(input)


# def test_day_10_part_2(input: str) -> None:
#     assert 8 == solve_day_part_2(input)

if __name__ == "__main__":
    real_input = DayInterface(10).get_day()
    print(real_input)
    test_day_10_part_1(test_input)
    # test_day_10_part_2(test_input)
    # print(DayInterface(9).submit_day(solve_day_part_2(real_input, 10), 2))
