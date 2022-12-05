from __future__ import annotations
import collections
from dataclasses import dataclass
import re
from typing import Self
from aoc_2022.utils.day_handler import DayInterface
from aoc_2022.utils.transforms import DataTransforms
import pytest

test_input = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""


@pytest.fixture
def input():
    return test_input


@dataclass
class Stack:
    stack: dict[int, list[str]]
    isntrs: list[Instr]

    @classmethod
    def from_str(cls, text: str, instrs: list[Instr]) -> Self:
        pattern = re.compile(r"(?P<index>[0-9]+)")
        lines = text.splitlines()
        index_locations = [
            (match.start("index"), int(match["index"])) for match in pattern.finditer(lines.pop())
        ]
        stack: collections.defaultdict[int, list[str]] = collections.defaultdict(list)
        for i, stack_num in index_locations:
            for line in lines:
                if line[i] != " ":
                    stack[stack_num].append(line[i])
        stack = {k: list(reversed(v)) for k, v in stack.items()}
        return cls(stack, instrs)

    def exec_instr(self, instr: Instr):
        for _ in range(instr.move):
            self.stack[instr.destination].append(self.stack[instr.current].pop())

    def exec_queue(self):
        """exec full instr queue"""
        for instr in self.isntrs:
            self.exec_instr(instr)

    @property
    def top_crates(self):
        return "".join(v.pop() for v in self.stack.values() if v)


@dataclass
class Instr:
    move: int
    current: int
    destination: int

    def __post_init__(self):
        if (
            isinstance(self.move, str)
            or isinstance(self.current, str)
            or isinstance(self.destination, str)
        ):
            self.move = int(self.move)
            self.current = int(self.current)
            self.destination = int(self.destination)

    @classmethod
    def from_instructions(cls, text: str) -> list[Self]:
        pattern = re.compile(
            r"move (?P<move>[0-9]+) from (?P<current>[0-9]+) to (?P<destination>[0-9]+)"
        )
        return [cls(**match.groupdict()) for match in pattern.finditer(text)]


def solve_day(input: str) -> str:
    stack, instructions = DataTransforms(input).header_footer
    instrs = Instr.from_instructions(instructions)
    stk = Stack.from_str(stack, instrs)
    stk.exec_queue()
    return stk.top_crates


def test_day_5_part_1(input: str) -> None:
    assert "CMZ" == solve_day(input)


if __name__ == "__main__":
    real_input = DayInterface(5).get_day()
    test_day_5_part_1(test_input)
    print(DayInterface(5).submit_day(solve_day(real_input)))
