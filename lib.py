import os
import subprocess
from pathlib import Path
from dataclasses import dataclass


@dataclass
class Matroska:
    mov_path: Path
    sub_path: Path = Path()

    def __init__(self, mov_path, sub_path=Path()):
        self.mov_path = mov_path

        if sub_path.suffix == ".srt":
            self.sub_path = sub_path
        else:
            ui = input(
                "No subtile file found in folder.\nWould you like to rip them from the video file? (y/n) » "
            )

            if ui.lower()[0] == "y":
                ui = input("Enter which stream you'd like to rip. » ")
                self.sub_path = self.ff_extract_subs(int(ui))
            else:
                self.sub_path = Path()

    def __str__(self):
        if self.sub_path == Path():
            return f"MATROSKA OBJECT {{\n\tFilename:\t{self.mov_path.name}\n\tSRT name:\tMISSING SRT FILE\n}}"
        else:
            return f"MATROSKA OBJECT {{\n\tFilename:\t{self.mov_path.name}\n\tSRT name:\t{self.sub_path.name}\n}}"

    def ff_swap_subs(
        self, aud_lang: str = "eng", sub_lang: str = "eng", aud_map: str = "0:a"
    ) -> None:
        """
        This method will create a new mkv file, in which a user
        provided subtitle track will replace the existing track(s).

        Parameters:
            output (str): The path to the output file
                aud_lang (str): Langugae of the audio stream
                    DEFAULT = "eng"
                sub_lang (str): Langugae of the subtitle track
                    DEFAULT = "eng"
                aud_map (str): Allows user to limit number of audio streams
                    DEFAULT = "0:a"
                    Example = "0:a:0" (Only map first audio stream)
        """

        output = str(self.mov_path).replace(".mkv", "_clean.mkv")

        subprocess.run(
            [
                "ffmpeg",
                "-i",
                self.mov_path,
                "-i",
                self.sub_path,
                # Keep all video & audio streams
                "-map",
                "0:v",
                "-map",
                aud_map,
                "-map_metadata",
                "0",
                # Everything else should be from new file
                "-map",
                "1",
                # Set languages of audio and subtitles to ENGLISH
                "-metadata:s:a:0",
                f"language={aud_lang}",
                "-metadata:s:s:0",
                f"language={sub_lang}",
                # Copy over everything mapped to stream 0
                "-c",
                "copy",
                # Copy over subtitles
                "-c:s",
                "srt",
                # Remove encoder information
                # "-fflags",
                # "+bitexact",
                # "-flags:v",
                # "+bitexact",
                # "-flags:a",
                # "+bitexact",
                output,
            ]
        )
        # self._clean_up()

    def ff_minimal_streams(
        self, aud_lang: str = "eng", sub_lang: str = "eng", sub_id: str = "0"
    ):
        output = str(self.mov_path).replace(".mkv", "_clean.mkv")

        subprocess.run(
            [
                "ffmpeg",
                "-i",
                self.mov_path,
                # Keep all video & first audio streams
                "-map",
                "0:v",
                "-map",
                "0:a:0",
                "-map",
                f"0:s:{sub_id}",
                "-map_metadata",
                "0",
                # Set languages of audio and subtitles to ENGLISH
                "-metadata:s:a:0",
                f"language={aud_lang}",
                "-metadata:s:s:0",
                f"language={sub_lang}",
                # Copy over everything mapped to stream 0
                "-c",
                "copy",
                # Remove encoder information
                "-fflags",
                "+bitexact",
                "-flags:v",
                "+bitexact",
                "-flags:a",
                "+bitexact",
                output,
            ]
        )
        # self._clean_up()

    def ff_extract_subs(self, id: int = 0) -> Path:
        """
        This method will extract the first subtitle track from
        the class instance.

        Paramters:
            id (int) : The id of the subtitle track you wish to extract
                defaults to 0 or the first track,
                1 would select the second track,
                etc...

        Returns:
            Extracts an SRT file from the class instance.
            Returns a the path to the extracted srt file as a string.
        """

        output = str(self.mov_path).replace(".mkv", ".srt")

        subprocess.run(
            [
                "ffmpeg",
                #  "-y",
                "-i",
                self.mov_path,
                "-c",
                "copy",
                "-map",
                f"0:s:{id}",
                output,
            ]
        )
        self.sub_path = Path(output)
        return self.sub_path

    def _clean_up(self):
        orig_name = str(self.mov_path)

        self.mov_path = Path(str(orig_name).replace(".mkv", "_clean.mkv"))

        # !!! FIGURE OUT HOW TO RENAME
        os.remove(self.sub_path)

        os.remove(orig_name)
        os.rename(self.mov_path, orig_name)


@dataclass
class SubtitleEntry:
    duration: str
    content: str


@dataclass
class Subtitle:
    path: Path
    entries: list[SubtitleEntry]

    url_bad = [
        "subtitles perfected",
        "subtitles by",
        "encoded by",
        "http:",
        "www.",
        ".org/",
        ".com/",
        ".net/",
    ]

    def __init__(self, sub_file: Path) -> None:
        """
        Provided a path to an SRT file, create a new Subtitle Object

        Patameters:
            sub_file (str) : path to SRT file
        """

        self.path = sub_file

        if not self.path.suffix == ".srt":
            return print("Cannot open subtitle file.")

        with open(self.path, "r") as file:
            raw_text: list[str] = file.read().strip().split("\n\n")

            self.entries: list[SubtitleEntry] = [
                SubtitleEntry(duration=line[1], content="\n".join(line[2:]))
                for line in [i.split("\n") for i in raw_text]
            ]

    def __len__(self):
        return len(self.entries)

    def __str__(self):
        file_name = self.path.name

        return f'SUBTITLE OBJECT {{\n\t"{file_name}"\n\t{len(self)} entries\n}}'

    def filter(self, bad_words: list[str] = url_bad) -> int:
        """
        Updates self.entries after removing any string
        listed in the [bad_words] list

        Parameters:
            bad_words (list[str]) : A list of strings
            Default value is a list of url artifacts

        Returns:
            int: Number of entries removed
        """

        orig_count: int = len(self)

        self.entries = [
            entry
            for entry in self.entries
            if not any(w in entry.content.lower() for w in bad_words)
        ]

        return orig_count - len(self)

    def update_srt(self) -> None:
        """
        Overwrites the existing srt file with whatever is stored in SELF.ENTRIES
        """

        with open(self.path, "w") as f:
            f.write(
                "\n\n".join(
                    [
                        f"{i+1}\n{entry.duration}\n{entry.content}"
                        for i, entry in enumerate(self.entries)
                    ]
                )
            )
        print("Succesfully overwrote old SRT file.")

    def quick_clean(self, bad_words: list[str] = url_bad) -> None:
        """
        Streamlines the FILTER & OUTPUT process

        Parameters:
            bad_words (list[str]) : A list of strings
            Default value is a list of url artifacts
        """

        removed: int = self.filter(bad_words)
        self.update_srt()
        print(f"Removed {removed} lines from SRT file.")
