import pathlib
import os

here = os.path.dirname(__file__)

template = here / pathlib.Path("../static/template.txt")

with open(template) as file:
    txt = file.read()


def write_file(path: str | pathlib.Path, day: int) -> None:
    with open(path, "w") as file:
        file.write(txt)
