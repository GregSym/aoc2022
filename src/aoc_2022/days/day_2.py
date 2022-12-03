from enum import Enum
from typing import NamedTuple
from aoc_2022.utils.day_handler import DayInterface
from aoc_2022.utils.transforms import DataTransforms
import pytest

test_input = """A Y
B X
C Z"""


class Outcomes(Enum):
    win: str = "win"
    lose: str = "lose"
    stalemate: str = "stalemate"


scoring = {Outcomes.win: 6, Outcomes.stalemate: 3, Outcomes.lose: 0}
item_scores = {"X": 1, "Y": 2, "Z": 3}
translator = {"A": "X", "B": "Y", "C": "Z"}
decrypt_outcome = {"X": Outcomes.lose, "Y": Outcomes.stalemate, "Z": Outcomes.win}


@pytest.fixture
def input():
    return test_input


class RockPaperScissors(NamedTuple):
    opp: str
    me: str

    @property
    def translated_opp(self) -> str:
        return translator[self.opp]

    def either_or(self, winning: str) -> int:
        if self.translated_opp == winning:
            return scoring[Outcomes.win] + item_scores[self.me]
        else:
            return scoring[Outcomes.lose] + item_scores[self.me]

    @property
    def winning_order(self):
        return ["Y", "X", "Z", "Y"]

    @property
    def item_beats_map(self):
        return {
            item: beats
            for item, beats in zip(self.winning_order, self.winning_order[1:])
        }

    @property
    def item_loses_map(self):
        return {
            item: loses
            for item, loses in zip(
                reversed(self.winning_order), [*reversed(self.winning_order)][1:]
            )
        }

    @property
    def desired_response(self):
        return {
            Outcomes.win: self.item_loses_map,
            Outcomes.lose: self.item_beats_map,
            Outcomes.stalemate: {self.translated_opp: self.translated_opp},
        }

    @property
    def score(self) -> int:
        if self.translated_opp == self.me:
            return scoring[Outcomes.stalemate] + item_scores[self.me]
        elif self.translated_opp != self.me:
            return self.either_or(self.item_beats_map[self.me])

    @property
    def decrypt(self) -> int:
        return (
            scoring[decrypt_outcome[self.me]]
            + item_scores[
                self.desired_response[decrypt_outcome[self.me]][self.translated_opp]
            ]
        )


def solve_day(input: str, part: int = 1):
    info = DataTransforms(input).pairs
    if part == 1:
        return sum([RockPaperScissors(opp, me).score for opp, me in info])
    else:
        return sum([RockPaperScissors(opp, me).decrypt for opp, me in info])


def test_day_2_part_1(input) -> None:
    assert 15 == solve_day(input)


def test_day_2_part_2(input) -> None:
    assert 12 == solve_day(input, 2)


if __name__ == "__main__":
    real_input = DayInterface(2).get_day()
    part = 2
    test_day_2_part_1(test_input)
    test_day_2_part_2(test_input)
    print(DayInterface(2).submit_day(solve_day(real_input, part), part=part))
