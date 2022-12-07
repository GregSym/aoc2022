from dataclasses import dataclass
import re
from typing import Self
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
        return r"(?P<name>[a-zA-Z0-9\.])"


@dataclass
class Dir(Response):
    @classmethod
    def from_response(cls, text: str) -> Self:
        pattern = re.compile(r"dir\s" + cls.name_part())
        return [cls(**match.groupdict()) for match in pattern.finditer(text)]


@dataclass
class File(Response):
    size: int

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


def solve_day(input: str) -> int:
    ...


def test_day_7_part_1(input: str) -> None:
    assert 95437 == solve_day(input)


if __name__ == "__main__":
    real_input = DayInterface(7).get_day()
    print(DayInterface(7).submit_day(solve_day(real_input)))
