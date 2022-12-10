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
    response: list[Response]

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


def tally(instructions: list[Instr]) -> int:
    edges: list[tuple[str, str]] = []
    sizes: dict[str, int] = {}
    for instr0, instr1 in zip(instructions, instructions[1:]):
        if "cd " in instr0.instruction and ".." not in instr0.instruction:
            parent = instr0.instruction.removeprefix("cd ")
            for dir in instr1.dirs:
                edges.append((parent, dir.name))
            explicit_size = sum([file.size for file in instr1.files])
            sizes[parent] = explicit_size
    
    @functools.lru_cache
    def _path(dir: str) -> list[str]:
        return [d for d in path(dir, edges)]
    
    # adding descendants' sizes
    for dirname in sizes:
        for dir in _path(dirname):
            if dir != dirname:
                sizes[dirname] += sizes[dir]
    return sum([size for size in sizes.values() if size <= 100_000])


def path(dirname: str, to_search: list[tuple[str, str]]) -> Generator[str, None, None]:
    yield dirname
    for i, edge in enumerate(to_search):
        if edge[0] == dirname:
            if i < len(to_search) - 1:
                for dir in path(edge[1], [*to_search[:i], *to_search[i + 1 :]]):
                    yield dir
            else:
                for dir in path(edge[1], [*to_search[:i]]):
                    yield dir


def solve_day(input: str) -> int:
    instrs = Instr.from_text(input)
    return tally(instrs)


def test_day_7_part_1(input: str) -> None:
    assert 95437 == solve_day(input)


if __name__ == "__main__":
    solve_day(test_input)
    test_day_7_part_1(test_input)
    real_input = DayInterface(7).get_day()
    print(DayInterface(7).submit_day(solve_day(real_input)))
