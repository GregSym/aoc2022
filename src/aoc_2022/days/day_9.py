import collections
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

    def __sub__(self, other: Self) -> Self:
        return type(self)(self.x - other.x, self.y - other.y)

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


def solve_day(input: str, part: int = 1) -> int:
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

def path_visualiser(path: list[Vector2D]):
    max_x = max([vec.x for vec in path])
    max_y = max([vec.y for vec in path])
    for i in range(max_y + 1, -1 * max_y - 2, -1):
        for j in range(-1 * max_x - 1, max_x + 2):
            if Vector2D(j,i) in path:
                print("T", end="")
            else:
                print(".", end="")
        print("")

def solve_day_part_2(input: str, knots: int = 10) -> int:
    info = [Instr(dir, int(delta)) for dir, delta in DataTransforms(input).tuples]
    origin = Vector2D(0, 0)
    paths = collections.defaultdict(lambda: [origin])
    for instr in info:
        for _ in range(instr.displacement):
            paths[0].append(paths[0][-1] + DIRECTIONS[instr.direction])
            for leading, trailing in zip(range(knots), range(1, knots)):
                if not paths[leading][-1].adjacent(paths[trailing][-1]):
                    # they have some dumb diagonal only movement rule for this one
                    if (
                        paths[leading][-1].x != paths[trailing][-1].x
                        and paths[leading][-1].y != paths[trailing][-1].y
                    ):
                        diff = paths[leading][-1] - paths[trailing][-1]
                        y_dir = diff.y // abs(diff.y)
                        x_dir = diff.x // abs(diff.x)
                        # paths[trailing].append(
                        #     paths[trailing][-1] + Vector2D(x_dir, y_dir)
                        # )
                        assert (
                            abs(diff.y) > 0
                            and abs(diff.x) > 0
                        ), f"{diff=}"
                        if abs(diff.x) == 1:
                            paths[trailing].append(
                                paths[trailing][-1]
                                + Vector2D(diff.x, y_dir * (abs(diff.y) - 1))
                            )
                        elif abs(diff.y) == 1:
                            paths[trailing].append(
                                paths[trailing][-1]
                                + Vector2D(x_dir * (abs(diff.x) - 1), diff.y)
                            )
                        else:
                            paths[trailing].append(
                                paths[trailing][-1]
                                + Vector2D(x_dir * (abs(diff.x) - 1), diff.y)
                            )
                            # assert abs(diff.x) == 2
                            # assert abs(diff.y) == 2
                            # paths[trailing].append(
                            #     paths[trailing][-1]
                            #     + Vector2D(x_dir, y_dir)
                            # )

                    else:
                        paths[trailing].append(paths[leading][-2])
    path_visualiser(paths[knots - 1])
    return len(set(paths[knots - 1]))


def test_day_9_part_1(input: str) -> None:
    assert 13 == solve_day(input)


def test_day_9_part_2(input: str) -> None:
    assert 13 == solve_day_part_2(input, 2)
    assert 1 == solve_day_part_2(input)
    example_1 = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""
    assert 36 == solve_day_part_2(example_1)


if __name__ == "__main__":
    # test_day_7_part_2(test_input)
    real_input = DayInterface(9).get_day()
    test_day_9_part_1(test_input)
    test_day_9_part_2(test_input)
    print(DayInterface(9).submit_day(solve_day_part_2(real_input, 10), 2))
