import collections
from enum import Enum
from typing import Generator
from aoc_2022.utils.day_handler import DayInterface
from aoc_2022.utils.transforms import DataTransforms
import pytest

test_input = """30373
25512
65332
33549
35390"""


@pytest.fixture
def input():
    return test_input


class Visible(Enum):
    left: str = "left"
    right: str = "right"
    top: str = "top"
    bottom: str = "bottom"


def solve_day(input: str) -> int:
    info = DataTransforms(input).heat_map_iterator
    row_tracker = collections.defaultdict(list)
    col_tracker = collections.defaultdict(list)
    cell_info = collections.defaultdict(list)
    for (x, y), num in info.items():
        row_tracker[x].append(num)
        if max(row_tracker[x]) == num and collections.Counter(row_tracker[x])[num] == 1:
            cell_info[(x, y)].append(Visible.left)
        col_tracker[y].append(num)
        if max(col_tracker[y]) == num and collections.Counter(col_tracker[y])[num] == 1:
            cell_info[(x, y)].append(Visible.top)
    row_tracker = collections.defaultdict(list)
    col_tracker = collections.defaultdict(list)
    for (x, y), num in reversed(info.items()):
        row_tracker[x].append(num)
        if max(row_tracker[x]) == num and collections.Counter(row_tracker[x])[num] == 1:
            cell_info[(x, y)].append(Visible.right)
        col_tracker[y].append(num)
        if max(col_tracker[y]) == num and collections.Counter(col_tracker[y])[num] == 1:
            cell_info[(x, y)].append(Visible.bottom)
    return sum([1 for k,v in cell_info.items() if v])


def test_day_8_part_1(input: str) -> None:
    assert 21 == solve_day(input)


# def test_day_7_part_2(input: str) -> None:
#     assert 24933642 == solve_day_part_2(input)


if __name__ == "__main__":
    # test_day_7_part_2(test_input)
    real_input = DayInterface(8).get_day()
    test_day_8_part_1(test_input)
    print(DayInterface(8).submit_day(solve_day(real_input)))
