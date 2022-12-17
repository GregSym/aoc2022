from dataclasses import dataclass
from typing import NamedTuple, Self
from aoc_2022.utils.day_handler import DayInterface
from aoc_2022.utils.transforms import DataTransforms
import pytest

test_input = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""


@pytest.fixture
def input():
    return test_input


@dataclass(unsafe_hash=True)
class Vector2D:
    x: int
    y: int

    def __mul__(self, num: int) -> Self:
        return type(self)(self.x * num, self.y * num)

    def __add__(self, other: Self) -> Self:
        return type(self)(self.x + other.x, self.y + other.y)
    
    def adjacent(self, other: Self) -> bool:
        return abs(self.x - other.x) <= 1 and abs(self.y - other.y) <= 1


DIRECTIONS = {
    "R": Vector2D(1, 0),
    "L": Vector2D(-1, 0),
    "U": Vector2D(0, 1),
    "D": Vector2D(0, -1),
}


class Instr(NamedTuple):
    direction: str
    displacement: int


def solve_day(input: str) -> int:
    info = [Instr(dir, int(delta)) for dir, delta in DataTransforms(input).tuples]
    origin = Vector2D(0, 0)
    head_path = [origin]
    tail_path = [origin]
    for instr in info:
        for i in range(instr.displacement):
            head_path.append(head_path[-1] + DIRECTIONS[instr.direction])
            if not head_path[-1].adjacent(tail_path[-1]):
                tail_path.append(head_path[-2])
    return len(set(tail_path))


def test_day_9_part_1(input: str) -> None:
    assert 13 == solve_day(input)


# def test_day_9_part_2(input: str) -> None:
#     assert 8 == solve_day_part_2(input)

if __name__ == "__main__":
    # test_day_7_part_2(test_input)
    real_input = DayInterface(9).get_day()
    test_day_9_part_1(test_input)
    # test_day_9_part_2(test_input)
    print(DayInterface(9).submit_day(solve_day(real_input)))
