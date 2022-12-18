# aoc2022

## Advent of Code 2022

### Contains simple helper lib

Started compiling a helper lib here (I'm doing a separate thing where I solve these in languages I don't know well enough (Rust for now), but I'm going to give up halfway through the month and just use python)
(maybe javascript)

But I'll attach an argsparse thing so it has the bare minimum amount of interoperability, maybe?

## is this a good helper lib for aoc, should I use it, etc?

no, lol. But you might wanna look at the implementation for your own. I'm not putting a lot of work into this, which makes it pretty simple to see what's happening.

There are several much better libraries if you want something with a finished cli or more comprehensive python implementation, etc.

### Here're 2 that probably work (haven't checked):

1. https://github.com/wimglenn/advent-of-code-data
1. https://youtu.be/CZZLCeRya74

## will there be a proper ci/cd setup at some point?

if they're doing an aoc2023 then maybe at that point

## setup

1. create a .env file for the session token (in the root of the working dir probably) - not currently handling anonymous sessions
   ```.ini
   [API]
   session=your_session_token
   ```
   (technically one could avoid the config style header with python's dotenv lib, not doing that right now)
   internally, we're doing the following to read it:
   ```python
   key = configparser.ConfigParser()
   key.read(".env")
   self.key = key.get("API", "session")
   ```
1. import the utils
   ```python
   from aoc_2022.utils.day_handler import DayInterface
   from aoc_2022.utils.transforms import DataTransforms
   ```
1. use the utils in a script
   ```python
   # get data
   aoc_interface = DayInterface(3)
   real_input = aoc_interface.get_day()
   # transform your data (bunch more options for some common patterns)
   info = DataTransforms(input).lines
   info = DataTransforms(input).group_lines(3)
   # do stuff
   # ...
   # test result
   # ...
   # submit
   aoc_interface.submit_day(solve_day(real_input))
   aoc_interface.submit_day(solve_day_part_2(real_input), 2)
   ```
1. use the cli (TODO! doesn't really have a lot of stuff going on yet)
   UNTESTED
   ```shell
   # seems to work
   # pull down data
   python -m aoc_2022.tools.cli get > some.txt
   # submit data
   python -m aoc_2022.tools.cli submit --day 3 --year 2022 --part 2 -s 594  # where -s is the solution
   python -m aoc_2022.tools.mkday_cli -d 11 -p ./path/to/days/day_11.py
   # creates a file with appropriate day numbering and testing segments
   # contains: solve function, 2 test functions, submit section
   ```
