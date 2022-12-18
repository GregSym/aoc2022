import collections
from dataclasses import dataclass
import itertools
import re
from typing import NamedTuple, Self
from aoc_2022.utils.day_handler import DayInterface
from aoc_2022.utils.transforms import DataTransforms
import pytest

test_input = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
"""

part_2_answer = """##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....
"""


@pytest.fixture
def input():
    return test_input


@dataclass
class Instr:
    name: str

    @classmethod
    def pattern(cls) -> re.Pattern[str]:
        return re.compile(f"(?P<name>{cls.__name__.lower()})")

    @classmethod
    def from_text(cls, text: str) -> list[Self]:
        return [cls(**match.groupdict()) for match in cls.pattern().finditer(text)]

    @property
    def cycles(self) -> int:
        return 2


class Noop(Instr):
    @property
    def cycles(self) -> int:
        return 1


@dataclass
class Add(Instr):
    reg: str
    value: int

    def __post_init__(self) -> None:
        if isinstance(self.value, str):
            self.value = int(self.value)

    @classmethod
    def pattern(cls) -> re.Pattern[str]:
        return re.compile(
            f"(?P<name>{cls.__name__.lower()})"
            + r"(?P<reg>[a-zA-Z0-9]+)\s*(?P<value>[0-9\-]+)"
        )


class Rect(NamedTuple):
    width: int = 40
    height: int = 6


CRT = Rect()


def solve_day(input: str) -> int:
    targets = [20, 60, 100, 140, 180, 220]
    info = DataTransforms(input).lines
    instrs: list[Instr] = [
        item
        for sublist in list(
            itertools.chain.from_iterable(
                [[option.from_text(line) for option in [Add, Noop]] for line in info]
            )
        )
        for item in sublist
    ]
    cycles = 1
    x = 1
    signal = 0
    signals: dict[int, int] = {}
    xlookups: dict[int, int] = {}
    for instr in instrs:
        for i in range(cycles, cycles + instr.cycles):
            signals[i] = i * x  # build signals
            xlookups[i] = x
            # print(xlookups[i], signals[i], i, instr)
        cycles += instr.cycles
        if isinstance(instr, Add):
            x += instr.value
        signal = cycles * x
    return sum([signals[target] for target in targets])


def visualise_screen(pixels: dict[tuple[int, int], str]) -> str:
    screen = ""
    for i in range(CRT.height):
        for j in range(CRT.width):
            screen += pixels[(j, i)]
        screen += "\n"
    return screen


def solve_day_part_2(input: str) -> str:
    targets = [20, 60, 100, 140, 180, 220]
    pixels = collections.defaultdict(lambda: ".")
    info = DataTransforms(input).lines
    instrs: list[Instr] = [
        item
        for sublist in list(
            itertools.chain.from_iterable(
                [[option.from_text(line) for option in [Add, Noop]] for line in info]
            )
        )
        for item in sublist
    ]
    cycles = 1
    x = 1
    signal = 0
    signals: dict[int, int] = {}
    xlookups: dict[int, int] = {}
    for instr in instrs:
        for i in range(cycles, cycles + instr.cycles):
            signals[i] = i * x  # build signals
            xlookups[i] = x
            pixels[((i - 1) % CRT.width, (i - 1) // CRT.width)] = (
                "#" if (i - 1) % CRT.width in [x - 1, x, x + 1] else "."
            )
            # print(xlookups[i], signals[i], i, instr)
        cycles += instr.cycles
        if isinstance(instr, Add):
            x += instr.value
        signal = cycles * x
    return visualise_screen(pixels)


def test_day_10_part_1(input: str) -> None:
    assert 13140 == solve_day(input)


def test_day_10_part_2(input: str) -> None:
    assert part_2_answer == solve_day_part_2(input)


if __name__ == "__main__":
    real_input = DayInterface(10).get_day()
    # print(real_input)
    test_day_10_part_1(test_input)
    test_day_10_part_2(test_input)
    print(solve_day_part_2(real_input))
    # print(DayInterface(10).submit_day(solve_day(real_input)))

    # submitted over cli
