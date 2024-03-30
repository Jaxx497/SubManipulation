import os
from os.path import isfile
from re import sub
import sys
import subprocess
from dataclasses import dataclass

from pathlib import Path


@dataclass
class Matroska:
    target: Path
    sub_path: Path

    def __init__(self, usr_path: str, sub_path: str | None = None) -> None:
        if sub_path is not None:
            if os.path.isfile(sub_path) and sub_path.endswith(".srt"):
                self.sub_path = Path(sub_path)

        if os.path.isfile(usr_path) and usr_path.endswith(".mkv"):
            self.target = Path(usr_path)

        elif os.path.isdir(usr_path):
            valid_mkv = [f for f in os.listdir(usr_path) if f.endswith(".mkv")]

            match len(valid_mkv):
                case 0:
                    sys.exit("No matroska files found in provided folder.")
                case 1:
                    mkv_path = os.path.join(usr_path, valid_mkv[0])
                    self.target = Path(mkv_path)
                case _:
                    print("Multiple mkv files found in dir")
                    print("TODO: USER MAKES A SELECTION")

            if sub_path is None:
                valid_sub = [s for s in os.listdir(usr_path) if s.endswith(".srt")]
                match len(valid_sub):
                    case 1:
                        print("FOUND PATH")
                        self.sub_path = Path(os.path.join(usr_path, valid_sub[0]))
                    case _:
                        print("ERROR FINDING SUB FILE")
                        self.sub_path = Path()
        else:
            sys.exit("NOT A VALID PATH TO MKV OR FOLDER")

    def ff_extract_subs(self, id: int = 0) -> Path:
        """
        This method will extract a subtitle track from
        the class instance.

        Paramters:
            id (int) : The id of the subtitle track to extract
                defaults to 0 or the first track,
                1 would select the second track,
                etc...

        Returns:
            Extracts an SRT file from the class instance.
            Returns a the path to the extracted srt file
            as a string.
        """

        output = str(self.target).replace(".mkv", ".srt")

        subprocess.run(
            [
                # "ffmpeg",
                # #  "-y",
                # "-i",
                # self.target,
                # "-c",
                # "copy",
                # "-map",
                # f"0:s:{id}",
                # output,
                "ffmpeg",
                "-i",
                self.target,
                "-map",
                f"0:s:{id}",
                "-c:s",
                "copy",
                output,
            ]
        )
        self.sub_path = Path(output)
        return self.sub_path
