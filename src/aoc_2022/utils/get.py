import datetime
import requests
import configparser


class DayInterface:
    def __init__(self, day: int = 1, year: int | None = None) -> None:
        key = configparser.ConfigParser()
        key.read(".env")
        key.get("API", "session")
        self.key = key.get("API", "session")
        self.day = day
        self.year = year if year is not None else datetime.datetime.now().year
        self.year_url = f"https://adventofcode.com/{self.year}/day"

    def get_day(self, day: int) -> str:
        def build_url(day: int, part: int) -> str:
            return f"{self.year_url}/{day}/input"

        res = requests.get(build_url(day, 1), cookies={"session": self.key})
        return res.text

    def submit_day(self, data: str | int | float) -> str:
        def build_url(day: int, part: int) -> str:
            return f"{self.year_url}/{day}/answer"

        res = requests.post(
            build_url(self.day), data=data, cookies={"session": self.key}
        )
