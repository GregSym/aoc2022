import collections
from dataclasses import dataclass
import functools
import re
from typing import Any, Generator, Self
from aoc_2022.utils.day_handler import DayInterface
from aoc_2022.utils.transforms import DataTransforms
import pytest

test_input = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""


@pytest.fixture
def input():
    return test_input


@dataclass
class Response:
    name: str

    @staticmethod
    def name_part() -> str:
        return r"(?P<name>[a-zA-Z0-9\.]+)"


@dataclass
class Dir(Response):
    @classmethod
    def from_response(cls, text: str) -> Self:
        pattern = re.compile(r"dir\s" + cls.name_part())
        return [cls(**match.groupdict()) for match in pattern.finditer(text)]


@dataclass
class File(Response):
    size: int

    def __post_init__(self) -> None:
        if isinstance(self.size, str):
            self.size = int(self.size)

    @classmethod
    def from_response(cls, text: str) -> Self:
        pattern = re.compile(r"(?P<size>[0-9]+)\s" + cls.name_part())
        return [cls(**match.groupdict()) for match in pattern.finditer(text)]


@dataclass
class Instr:
    instruction: str
    response: str

    @property
    def files(self) -> list[File]:
        return File.from_response(self.response)

    @property
    def dirs(self) -> list[Dir]:
        return Dir.from_response(self.response)

    @classmethod
    def from_text(cls, text: str) -> list[Self]:
        pattern = re.compile(r"\$ (?P<instruction>[^\n]+)\n(?P<response>[^$]*)")
        return [cls(**match.groupdict()) for match in pattern.finditer(text)]


def tally(instructions: list[Instr], part: int = 1) -> int:
    sizes: dict[str, int] = collections.defaultdict(int)
    dir_stack = []
    for instr0, instr1 in zip(instructions, instructions[1:]):
        if "cd " in instr0.instruction:
            if ".." in instr0.instruction:
                dir_stack.pop()
            else:
                dir_stack.append(instr0.instruction.removeprefix("cd "))
            for i, dir in enumerate(dir_stack):
                explicit_size = sum([file.size for file in instr1.files])
                sizes["/".join(dir_stack[:i]) + f"/{dir}"] += explicit_size
    if part == 1:
        return sum([size for size in sizes.values() if size <= 100_000])
    if part == 2:
        return min(
            [
                size
                for size in sizes.values()
                if size >= 30000000 - (70000000 - sizes["//"])
            ]
        )


def solve_day(input: str) -> int:
    instrs = Instr.from_text(input)
    return tally(instrs)


def solve_day_part_2(input: str) -> int:
    instrs = Instr.from_text(input)
    return tally(instrs, 2)


def test_day_7_part_1(input: str) -> None:
    assert 95437 == solve_day(input)


def test_day_7_part_2(input: str) -> None:
    assert 24933642 == solve_day_part_2(input)


if __name__ == "__main__":
    test_day_7_part_1(test_input)
    test_day_7_part_2(test_input)
    real_input = DayInterface(7).get_day()
    print(DayInterface(7).submit_day(solve_day_part_2(real_input), 2))
