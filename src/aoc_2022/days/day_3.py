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
    total = 0
    for group in info:
        sacks = []
        for sack in group:
            sacks.append(collections.Counter(sack))
        all_badges = {badge for sack in sacks for badge in sack}
        for badge in all_badges:
            if badge in sacks[0] and badge in sacks[1] and badge in sacks[2]:
                total += priorities[badge]
    return total


def test_day3_part_1(input) -> None:
    assert 157 == solve_day(input)


def test_day3_part_2(input) -> None:
    assert 70 == solve_day_part_2(input)


if __name__ == "__main__":
    real_input = DayInterface(3).get_day()
    test_day3_part_1(test_input)
    test_day3_part_2(test_input)
    print(DayInterface(3).submit_day(solve_day_part_2(real_input), 2))
