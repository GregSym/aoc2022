import pathlib
import os
import re

here = os.path.dirname(__file__)

template = here / pathlib.Path("../static/template.txt")



def write_file(path: str | pathlib.Path, day: int) -> None:
    with open(template) as file:
        txt = file.read()
    txt = re.sub(r"DayInterface\([0-9]+\)", f"DayInterface({day})", txt)
    txt = re.sub(r"day\_[0-9]+", f"day_{day}", txt)
    with open(path, "w") as file:
        file.write(txt)
