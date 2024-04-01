import os
import sys
import subprocess
from dataclasses import dataclass

from pathlib import Path


@dataclass
class Matroska:
    target: Path
    sub_path: Path | None

    def __init__(self, usr_path: str, sub_path: str | None = None) -> None:
        if sub_path is not None:
            if os.path.isfile(sub_path) and sub_path.endswith(".srt"):
                self.sub_path = Path(sub_path)
        # else:
        #     self.sub_path = sub_path

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
                valid_sub = [
                    sub for sub in os.listdir(usr_path) if sub.endswith(".srt")
                ]
                match len(valid_sub):
                    case 1:
                        self.sub_path = Path(os.path.join(usr_path, valid_sub[0]))
                    case _:
                        print("ERROR FINDING SUB FILE")
                        self.sub_path = sub_path
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
                "ffmpeg",
                "-i",
                self.target,
                "-map",
                f"0:s:{id}",
                "-c:s",
                "copy",
                "-y",
                output,
            ]
        )
        self.sub_path = Path(output)
        return self.sub_path

    # Parameters will be handled by cmdline args
    def ffmpeg_bulider(
        self, aud_lang: str = "eng", aud_id: str = "0", sub_id: str = "0"
    ):
        # Assign mkv file as first input
        prompt = ["ffmpeg", "-i", self.target]

        # If sub_path is valid, it is the second input
        if self.sub_path is not None:
            prompt.extend(["-i", self.sub_path])

        # Map video and FIRST audio track and chapters
        prompt.extend(
            [
                "-map",
                "0:v",
                "-map",
                f"0:a:{aud_id}",
                "-map_metadata",
                "-1",
                "-map_chapters",
                "0",
            ]
        )

        # Handle languages of FIRST audio/sub:
        prompt.extend(
            [
                "-metadata:s:a:0",
                f"language={aud_lang}",
                "-metadata:s:s:0",
                "language=eng",
            ]
        )

        # If a subtitle input is valid, copy it in
        if self.sub_path is not None:
            prompt.extend(["-map", "1", "-c", "copy", "-c:s", "srt"])
        # Otherwise, map the specified subtitle ID to the only
        else:
            prompt.extend(["-map", f"0:s:{sub_id}", "-c", "copy"])

        # Remove encoder information:
        prompt.extend(
            [
                "-disposition:s:0",
                "default",
                "-fflags",
                "+bitexact",
                "-flags:v",
                "+bitexact",
                "-flags:a",
                "+bitexact",
                str(self.target).replace(".mkv", "_clean.mkv"),
            ]
        )

        subprocess.run(prompt)
