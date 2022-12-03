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
    def group_lines(self, number: int) -> list[list[str]]:
        ...
