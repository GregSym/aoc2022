import re
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


class Ranges:
    def __init__(self, start0, end0, start1, end1) -> None:
        self.start0 = int(start0)
        self.end0 = int(end0)
        self.start1 = int(start1)
        self.end1 = int(end1)


def solve_day(input: str, part: int = 1) -> int:
    info = DataTransforms(input).lines
    pattern = re.compile(
        r"(?P<start0>[0-9]+)\-(?P<end0>[0-9]+),(?P<start1>[0-9]+)\-(?P<end1>[0-9]+)"
    )
    overlaps = 0
    for elf_pair in info:
        ranges = Ranges(**pattern.match(elf_pair).groupdict())
        range0 = set([*range(ranges.start0, ranges.end0 + 1)])
        range1 = set([*range(ranges.start1, ranges.end1 + 1)])
        if part == 1:
            if range1.issubset(range0) or range0.issubset(range1):
                overlaps += 1
        else:
            if range1.intersection(range0) != set():
                overlaps += 1
    return overlaps


def test_day_4_part_1(input: str):
    assert 2 == solve_day(input)


def test_day_4_part_2(input: str):
    assert 4 == solve_day(input, 2)


if __name__ == "__main__":
    real_input = DayInterface(4).get_day()
    test_day_4_part_1(test_input)
    test_day_4_part_2(test_input)
    print(DayInterface(4).submit_day(solve_day(real_input, 2), 2))
