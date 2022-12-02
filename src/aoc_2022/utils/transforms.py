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
