import collections
from enum import Enum
from math import prod
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


# there were actually mistakes in part 1 that accidentally _didn't_ break it
def solve_day(input: str) -> int:
    info = DataTransforms(input).heat_map_iterator
    row_tracker = collections.defaultdict(list)
    col_tracker = collections.defaultdict(list)
    cell_info = collections.defaultdict(list)
    for (x, y), num in info.items():
        row_tracker[y].append(num)
        if max(row_tracker[y]) == num and collections.Counter(row_tracker[y])[num] == 1:
            cell_info[(x, y)].append(Visible.left)
        col_tracker[x].append(num)
        if max(col_tracker[x]) == num and collections.Counter(col_tracker[x])[num] == 1:
            cell_info[(x, y)].append(Visible.top)
    row_tracker = collections.defaultdict(list)
    col_tracker = collections.defaultdict(list)
    for (x, y), num in reversed(info.items()):
        row_tracker[y].append(num)
        if max(row_tracker[y]) == num and collections.Counter(row_tracker[y])[num] == 1:
            cell_info[(x, y)].append(Visible.right)
        col_tracker[x].append(num)
        if max(col_tracker[x]) == num and collections.Counter(col_tracker[x])[num] == 1:
            cell_info[(x, y)].append(Visible.bottom)
    return sum([1 for v in cell_info.values() if v])


def solve_day_part_2(input: str) -> int:
    info = DataTransforms(input).heat_map_iterator
    row_tracker = collections.defaultdict(list)
    col_tracker = collections.defaultdict(list)
    cell_info = collections.defaultdict(list)
    for (x, y), num in info.items():
        row_tracker[y].append(num)
        if max(row_tracker[y]) == num and collections.Counter(row_tracker[y])[num] == 1:
            cell_info[(x, y)].append(Visible.left)
        col_tracker[x].append(num)
        if max(col_tracker[x]) == num and collections.Counter(col_tracker[x])[num] == 1:
            cell_info[(x, y)].append(Visible.top)
    row_tracker = collections.defaultdict(list)
    col_tracker = collections.defaultdict(list)
    for (x, y), num in reversed(info.items()):
        row_tracker[y].append(num)
        if max(row_tracker[y]) == num and collections.Counter(row_tracker[y])[num] == 1:
            cell_info[(x, y)].append(Visible.right)
        col_tracker[x].append(num)
        if max(col_tracker[x]) == num and collections.Counter(col_tracker[x])[num] == 1:
            cell_info[(x, y)].append(Visible.bottom)

    row_len = len(DataTransforms(input).heat_map[0])
    col_len = len(DataTransforms(input).heat_map)
    cell_score = collections.defaultdict(list)

    def search_space(x, y, horizontal: bool = True, *ran_args):
        score = 0
        for i in range(*ran_args):
            if horizontal and info[(i, y)] < info[(x, y)]:
                score = abs(x - i) if horizontal else abs(y - i)
            elif not horizontal and info[(x, i)] < info[(x, y)]:
                score = abs(x - i) if horizontal else abs(y - i)
            else:
                break
        cell_score[(x,y)].append(score + 1)

    for (x, y), num in info.items():
        if cell_info[(x, y)]:
            if Visible.left in cell_info[(x, y)]:
                cell_score[(x,y)].append(x)
            else:
                search_space(x, y, True, *(x - 1, 0 - 1, -1))
            if Visible.right in cell_info[(x, y)]:
                cell_score[(x,y)].append(row_len - x - 1)
            else:
                search_space(x, y, True, *(x + 1, row_len))
            if Visible.top in cell_info[(x, y)]:
                cell_score[(x,y)].append(y)
            else:
                search_space(x, y, False, *(y - 1, 0 - 1, -1))
            if Visible.bottom in cell_info[(x, y)]:
                cell_score[(x,y)].append(col_len - y - 1)
            else:
                search_space(x, y, False, *(y + 1, col_len))
        else:
            search_space(x, y, True, *(x - 1, 0 - 1, -1))
            search_space(x, y, True, *(x + 1, row_len))
            search_space(x, y, False, *(y - 1, 0 - 1, -1))
            search_space(x, y, False, *(y + 1, col_len))
        assert len(cell_score[(x,y)]) == 4
    return max([prod(s) for s in cell_score.values()])


def test_day_8_part_1(input: str) -> None:
    assert 21 == solve_day(input)


def test_day_8_part_2(input: str) -> None:
    assert 8 == solve_day_part_2(input)


if __name__ == "__main__":
    # test_day_7_part_2(test_input)
    real_input = DayInterface(8).get_day()
    test_day_8_part_1(test_input)
    test_day_8_part_2(test_input)
    print(DayInterface(8).submit_day(solve_day_part_2(real_input), 2))
