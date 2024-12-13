import datetime
import re
import requests
import configparser


class DayHomepage:
    def __init__(self, day: int = 1, year: int | None = None) -> None:
        key = configparser.ConfigParser()
        key.read(".env")
        self.key = key.get("API", "session")
        self.day = day
        self.year = year if year is not None else datetime.datetime.now().year
        self.year_url = f"https://adventofcode.com/{self.year}/day"

    @property
    def url(self) -> str:
        return f"{self.year_url}/{self.day}"

    def get_day(self) -> str:
        res = requests.get(self.url, cookies={"session": self.key})
        if res.status_code == 200:
            return res.text
        else:
            return f"BAD_RESPONSE_{res.status_code}"

    @property
    def past_answers(self) -> list[int | str]:
        body = self.get_day()
        pattern = re.compile(r"Your puzzle answer was \<code\>(?P<answer>[^\<]*?)\<")
        return [
            int(m["answer"]) if m["answer"].isdigit() else m["answer"]
            for m in pattern.finditer(body)
        ]


class DayInterface:
    def __init__(self, day: int = 1, year: int | None = None) -> None:
        key = configparser.ConfigParser()
        key.read(".env")
        self.key = key.get("API", "session")
        self.day = day
        self.year = year if year is not None else datetime.datetime.now().year
        self.year_url = f"https://adventofcode.com/{self.year}/day"
    
    @property
    def homepage(self) -> DayHomepage:
        return DayHomepage(day=self.day, year=self.year)

    def get_day(self) -> str:
        def build_url(day: int) -> str:
            return f"{self.year_url}/{day}/input"

        res = requests.get(build_url(self.day), cookies={"session": self.key})
        return res.text
    
    def submit_day(self, data: str | int | float, part: int = 1) -> str | tuple[requests.Response, str]:
        def build_url(day: int) -> str:
            return f"{self.year_url}/{day}/answer"

        res = requests.post(
            build_url(self.day),
            data={"level": part, "answer": data},
            cookies={"session": self.key},
        )

        if len(self.homepage.past_answers) >= 1 and part == 1:
            if self.homepage.past_answers[0] == data:
                return "you've submitted that answer previously, it was correct"
            else:
                return "you've answered before, but this submission is wrong"
        elif len(self.homepage.past_answers) >= 2 and part == 2:
            if self.homepage.past_answers[1] == data:
                return "you've submitted that answer previously, it was correct"
            else:
                return "you've answered before, but this submission is wrong"

        key_phrases = [
            "That's the right answer!",
            "Both parts of this puzzle are complete!",
            "You don\'t seem to be solving the right level.  Did you already complete it?"
        ]
        for phrase in key_phrases:
            if phrase in res.text:
                return phrase
        wait_time = re.search(r"You have (?P<secs>[0-9]+)s left to wait", res.text)
        if wait_time is not None:
            return f"""You submitted too recently. 
            You have {wait_time['secs']}s left to wait. 
            (try not to spam their site)"""
        hint = re.search(
            r"That\'s not the right answer\; (?P<hint>[^\.]*)\."
            "|"
            r"Because you have guessed incorrectly (?P<guesses>[0-9]+)"
            r" times on this puzzle, please wait (?P<minutes>[0-9]+) minutes before trying again."
            "|"
            r"You gave an answer too recently; "
            r"you have to wait after submitting an answer before trying again.  "
            r"You have (?P<minutes_alt>[0-9]+)m (?P<secs>[0-9]+)s left to wait.",
            res.text,
        )
        if hint is not None:
            return hint[0]
        return res, res.text
