import argparse
from datetime import datetime
from typing import Any, NamedTuple, Self
from aoc_2022.utils.day_handler import DayInterface
from aoc_2022.utils.mkday import write_file


class AocArgs(NamedTuple):
    day: int
    year: int

    @classmethod
    def populate_from_args(cls, args: argparse.Namespace) -> Self:
        day = datetime.now().day % 25
        day = 25 if day == 0 else day  # 1 - 25
        return cls(
            args.day if args.day is not None else day,
            args.year if args.year is not None else datetime.now().year,
        )


class SubmissionArgs(NamedTuple):
    data: Any
    part: int = 1

    @classmethod
    def populate_from_args(cls, args: argparse.Namespace) -> Self:
        return cls(
            args.submission,
            args.part if args.part is not None else 1,
        )


def main(args: argparse.Namespace) -> int:
    if args.mode == "get":
        print(DayInterface(*AocArgs.populate_from_args(args)).get_day())
    elif args.mode == "submit":
        print(
            DayInterface(*AocArgs.populate_from_args(args)).submit_day(
                *SubmissionArgs.populate_from_args(args)
            )
        )
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Handling data grepping and submission to advent of code"
    )
    parser.add_argument("mode")
    parser.add_argument("-y", "--year")
    parser.add_argument("-d", "--day")
    parser.add_argument("-p", "--part")
    parser.add_argument("-s", "--submission")
    args = parser.parse_args()
    main(args)
