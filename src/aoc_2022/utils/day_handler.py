import datetime
import re
import requests
import configparser


class DayInterface:
    def __init__(self, day: int = 1, year: int | None = None) -> None:
        key = configparser.ConfigParser()
        key.read(".env")
        self.key = key.get("API", "session")
        self.day = day
        self.year = year if year is not None else datetime.datetime.now().year
        self.year_url = f"https://adventofcode.com/{self.year}/day"

    def get_day(self) -> str:
        def build_url(day: int) -> str:
            return f"{self.year_url}/{day}/input"

        res = requests.get(build_url(self.day), cookies={"session": self.key})
        return res.text

    def submit_day(self, data: str | int | float, part: int = 1) -> str:
        def build_url(day: int) -> str:
            return f"{self.year_url}/{day}/answer"

        res = requests.post(
            build_url(self.day), data={"level": part, "answer": data}, cookies={"session": self.key}
        )

        key_phrases = ["That\'s the right answer!"]
        for phrase in key_phrases:
            if phrase in res.text:
                return phrase
        wait_time = re.search(r"You have (?P<secs>[0-9]+)s left to wait", res.text)
        if wait_time is not None:
            return f"""You submitted too recently. 
            You have {wait_time}s left to wait. 
            (try not to spam their site)"""
        return res, res.text
