import collections


class DataTransforms:
    def __init__(self, data: str) -> None:
        self.data = data

    @property
    def sectioned_numbers(self) -> list[list[int | float]]:
        sectioned = self.data.split("\n\n")
        return [
            [
                int(entry) if "." not in entry else float(entry)
                for entry in section.splitlines()
            ]
            for section in sectioned
        ]

    @property
    def pairs(self) -> tuple[str, str]:
        return [tuple(pair.split()) for pair in self.data.splitlines()]

    @property
    def lines(self) -> list[str]:
        return self.data.splitlines()

    @property
    def header_footer(self) -> tuple[str, str]:
        return self.data.split("\n\n")

    def group_lines(self, number: int) -> list[tuple[str]]:
        grouped = [
            lines for lines in zip(*[self.data.splitlines()[i:] for i in range(number)])
        ]
        return [grouped[i] for i in range(0, len(grouped), number)]

    @property
    def heat_map(self) -> list[list[int]]:
        outer = []
        for row in self.data.splitlines():
            inner = []
            for num in row:
                inner.append(int(num))
            outer.append(inner)
        return outer

    @property
    def heat_map_iterator(self):
        safe_indexer: dict[tuple[int, int], int] = collections.defaultdict(int)
        for i, row in enumerate(self.data.splitlines()):
            for j, num in enumerate(row):
                safe_indexer[(j,i)] = int(num)  # x,y for the key, y like pixels
        return safe_indexer
    