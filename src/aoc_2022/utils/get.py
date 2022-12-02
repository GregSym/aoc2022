import requests
import configparser

def get_day(day: int) -> str:
    key = configparser.ConfigParser()
    key.read(".env")
    key.get("API", "session")

    def build_url(day: int, part: int) -> str:
        return f"https://adventofcode.com/2022/day/{day}/input"

    res = requests.get(build_url(1,1),cookies={"session":key.get("API", "session")})
    return res.text