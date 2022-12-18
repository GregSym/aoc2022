import argparse

from aoc_2022.utils.mkday import write_file


def main(args: argparse.Namespace) -> int:
    write_file(args.path, int(args.day))
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a file for solving a of advent of code"
    )
    parser.add_argument("-y", "--year")
    parser.add_argument("-d", "--day")
    parser.add_argument("-l", "--language", default="python")
    parser.add_argument("-p", "--path")
    args = parser.parse_args()
    raise SystemExit(main(args))
