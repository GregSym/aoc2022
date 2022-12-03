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

    def group_lines(self, number: int) -> list[tuple[str]]:
        grouped = [lines for lines in zip(*[self.data[i:] for i in number])]
        return [grouped[i] for i in range(0, len(grouped), number)]
