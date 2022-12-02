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

def test_day_1_part_1(input: str):
    assert 24000 == solve_day(input)


if __name__ == "__main__":
    real_input = DayInterface(1).get_day()
    test_day_1_part_1(test_input)
    print(solve_day(real_input))
    print(DayInterface(1).submit_day(solve_day(real_input)))
