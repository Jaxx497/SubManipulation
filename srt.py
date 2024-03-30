from dataclasses import dataclass
from pathlib import Path


@dataclass
class Caption:
    duration: str
    content: str


@dataclass
class Subtitle:
    path: Path
    subs: list[Caption]

    def __init__(self, path) -> None:
        with open(path, "r") as file:
            raw_text: list[str] = file.read().strip().split("\n\n")

            self.entries: list[Caption] = [
                Caption(duration=line[1], content="\n".join(line[2:]))
                for line in [i.split("\n") for i in raw_text]
            ]
