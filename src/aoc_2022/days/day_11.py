import ast
from dataclasses import dataclass
import re
from typing import Callable, Self
from aoc_2022.utils.day_handler import DayInterface
from aoc_2022.utils.transforms import DataTransforms
import pytest

test_input = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""


@pytest.fixture
def input():
    return test_input


@dataclass
class Monkey:
    id: int
    items: list[int]
    operation: Callable[[int], int]
    test: Callable[[int], bool]
    actions: dict[bool, int]
    inspections: int = 0

    def __post_init__(self) -> None:
        # evaluation is a little dicey here
        if isinstance(self.items, int):
            self.items = [self.items]
        elif isinstance(self.items, tuple):
            self.items = [*self.items]

    @classmethod
    def from_text(cls, text: str) -> list[Self]:
        pattern = re.compile(
            r"Monkey\s*(?P<id>[0-9]+)\:[\s\S]*?\:\s*(?P<items>[0-9\,\s]+)"
            r"Operation\:\s*new\s*\=\s*(?P<operation>[^\n]+)"
            r"\s*"
            r"Test\:\s*divisible by\s*(?P<test>[0-9]+)"
            r"\s*"
            r"If true\:\s*throw to monkey\s*(?P<action_true>[0-9]+)"
            r"\s*"
            r"If false\:\s*throw to monkey\s*(?P<action_false>[0-9]+)"
        )
        monkeys: list[Self] = []
        for match in pattern.finditer(text):
            items = ast.literal_eval(match["items"].strip())
            operation = eval(
                "lambda old: " + match["operation"].strip()
            )  # haha, evil stuff
            test = lambda item: item // int(match["test"]) == item / int(match["test"])
            actions = {
                True: int(match["action_true"]),
                False: int(match["action_false"]),
            }
            monkeys.append(cls(int(match["id"]), items, operation, test, actions))
        return monkeys



def solve_day(input: str) -> int:
    info = input  # no manipulation necessary
    monkeys = Monkey.from_text(info)
    for round in range(20 // 4):
        for monkey in monkeys:
            empty = []
            for i, item in enumerate(monkey.items):
                item = monkey.operation(item) // 3
                test = monkey.test(item)
                monkeys[monkey.actions[test]].items.append(item)
                empty.append(i)
                monkey.inspections += 1
            for j in reversed(empty):
                monkey.items.pop(j)
    monkeys = sorted(monkeys, key=lambda monk: monk.inspections)
    print(monkeys)
    return sum([monkey.inspections for monkey in monkeys[-2:]])


def test_day_11_part_1(input: str) -> None:
    # test solution to part 1
    assert 10605 == solve_day(input)


# def test_day_11_part_2(input: str) -> None:
#    # test solution to part 2
#    assert 19 == solve_day(input)


if __name__ == "__main__":
    real_input = DayInterface(11).get_day()
    test_day_11_part_1(test_input)
    # test_day_11_part_2(test_input)
    print(DayInterface(11).submit_day(solve_day(real_input)))
