from aoc_2022.utils.get import DayInterface
from aoc_2022.utils.transforms import DataTransforms
import pytest

test_input = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""


@pytest.fixture
def input():
    return test_input

def solve_day(input: str):
    info = DataTransforms(input).sectioned_numbers
    section_sums = {i: sum(section) for i, section in enumerate(info)}
    return max([total for total in section_sums.values()])

def solve_day_part_2(input: str):
    info = DataTransforms(input).sectioned_numbers
    section_sums = sorted([sum(section) for section in info], reverse=True)
    return sum(section_sums[:3])

def test_day_1_part_1(input: str):
    assert 24000 == solve_day(input)
def test_day_1_part_2(input: str):
    assert 45000 == solve_day_part_2(input)


if __name__ == "__main__":
    real_input = DayInterface(1).get_day()
    test_day_1_part_1(test_input)
    test_day_1_part_2(test_input)
    print(solve_day(real_input))
    # print(DayInterface(1).submit_day(solve_day(real_input), 1))
    print(DayInterface(1).submit_day(solve_day_part_2(real_input), 2))
