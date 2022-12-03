import collections
from aoc_2022.utils.day_handler import DayInterface
from aoc_2022.utils.transforms import DataTransforms
import pytest

test_input = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""

lowercase = "abcdefghijklmnopqrstuvwxyz"
uppercase = lowercase.upper()
priorities = {l: p for l, p in zip([*lowercase, *uppercase], range(1, 52 + 1))}


@pytest.fixture
def input():
    return test_input


def solve_day(input: str):
    info = DataTransforms(input).lines
    total = 0
    for sack in info:
        part_1 = collections.Counter(sack[: len(sack) // 2])
        part_2 = collections.Counter(sack[len(sack) // 2 :])
        for item in part_1:
            if item in part_2:
                total += priorities[item]
    return total

def solve_day_part_2(input: str):
    info = DataTransforms(input).group_lines(3)
    for group in info:
        for sack in group:...

def test_day3_part_1(input) -> None:
    assert 157 == solve_day(input)


if __name__ == "__main__":
    real_input = DayInterface(3).get_day()
    test_day3_part_1(test_input)
    print(DayInterface(3).submit_day(solve_day(real_input)))
