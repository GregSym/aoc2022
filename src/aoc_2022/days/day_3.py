from enum import Enum
from typing import NamedTuple
from aoc_2022.utils.get import DayInterface
from aoc_2022.utils.transforms import DataTransforms
import pytest

test_input = """A Y
B X
C Z"""

@pytest.fixture
def input():
    return test_input

if __name__ == "__main__":
    print(DayInterface(3).get_day())