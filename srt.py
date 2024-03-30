import os
import sys
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

    KILL_LIST = {
        "subtitles perfected",
        "subtitles by",
        "encoded by",
        "http",
        "www",
        ".org",
        ".com",
        ".net",
    }

    def __init__(self, path: str | Path) -> None:
        # Try to open Path
        if not os.path.exists(path):
            print("ERROR: Provided path to subtitle was invalid.")
            sys.exit(1)

        path = self.path = Path(path)

        with open(path, "r") as file:
            raw_text: list[str] = file.read().strip().split("\n\n")
            self.path: Path = Path(path)
            self.entries: list[Caption] = [
                Caption(duration=line[1], content="\n".join(line[2:]))
                for line in [i.split("\n") for i in raw_text]
            ]

    def clean(self, bad_words: set[str] = KILL_LIST) -> None:
        """
        Streamlines the FILTER & OUTPUT process

        Parameters:
            bad_words (list[str]) : A list of strings
            Default value is a list of url artifacts
        """

        removed: int = self._filter(bad_words)
        self._update_srt()
        print(f"Removed {removed} lines from SRT file.")

    def _filter(self, bad_words: set[str] = KILL_LIST) -> int:
        """
        Updates self.entries after removing any string
        listed in the [bad_words] list

        Parameters:
            bad_words (list[str]) : A list of strings
            Default value is a list of url artifacts

        Returns:
            int: Number of entries removed
        """

        orig_count: int = len(self.entries)

        self.entries = [
            caption
            for caption in self.entries
            if not any(word in caption.content.lower() for word in bad_words)
        ]

        return orig_count - len(self.entries)

    def _update_srt(self) -> None:
        """
        Overwrites the existing srt file with whatever
        is stored in SELF.ENTRIES
        """

        with open(self.path, "w") as f:
            f.write(
                "\n\n".join(
                    [
                        f"{idx+1}\n{caption.duration}\n{caption.content}"
                        for idx, caption in enumerate(self.entries)
                    ]
                )
            )
        print("Succesfully overwrote old SRT file.")
