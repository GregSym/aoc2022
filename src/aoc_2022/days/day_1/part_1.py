from aoc_2022.utils.get import get_day
from aoc_2022.utils.transforms import DataTransforms
import pytest

@pytest.fixture
def input():
    return """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""


def test_day_1_part_1(input: str):
    info = DataTransforms(input).sectioned_numbers
    section_sums = {i:sum(section) for i,section in enumerate(info)}
    assert 24000 == max([total for total in section_sums.values()])


if __name__ == "__main__":
    real_input = get_day(1)
