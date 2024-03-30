# from pathlib import Path
from mkv import Matroska

# from srt import Subtitle
from mkv import Matroska


class COLORS:
    DEFAULT = "\033[1;37m"
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    TEMP = "\u001b[38;2;145;231;255m"


def main():
    # test_file = "./src/gb2.srt"
    # x = Subtitle(test_file)
    # print(x.path)

    # test_mkv = r"M:\High and Low (1963) [1080p x265 10bit DTS-4] (9.76 GB)\High.and.Low.1963.CC.1080p.BluRay.x265.10bit.DTS-ADE.mkv"
    test_mkv = r"M:\High and Low (1963) [1080p x265 10bit DTS-4] (9.76 GB)"

    # test_mkv = r"M:\Being John Malkovich (1999) [1080p x265 10bit AAC-5.1] (4.75 GB)\Being John Malkovich (1999) Criterion (1080p BluRay x265 10bit Tigole).mkv"
    # test_mkv = "M:\\Being John Malkovich (1999) [1080p x265 10bit AAC-5.1] (4.75 GB)"  # Valid folder with one mkv
    # test_mkv = "C:\\Users\\J\\Desktop\\py-movie-review"  # Valid folder, no mkv
    # test_mkv = r"C:\Users\J\Desktop\mrsnicks.jpg"  # Invalid file

    x = Matroska(
        test_mkv,
    )
    print(x.target)
    print(x.sub_path)
    # x.ff_extract_subs()


"""
# -- ROADMAP -- #
1. Read in subtitle track
    x Make sure it's a path
    - Make sure it's a valid subtitle file

2. Recreate Matroska class
    - Create sub extraction
    - Figure out better way to read folders

3. Streamline FFMPEG Wrapping

4. Implement cmdline args

5. Implement SSA/ASS Editing
    - (Looking into this, we can probably
    just use ffmpeg to convert SSA into SRT)

"""

# ! I really like the idea of adding a spellchecker but
#   I'm having problems implementing something that works.
#   The problem comes up with proper nouns causing false
#   positives making it harder to parse information.
#

# from spellchecker import SpellChecker
# def spell_check(sub_track: Subtitle):
#     checker = SpellChecker(language="en", case_sensitive=False)
#
#     for i, sub in enumerate(sub_track.entries, 1):
#         text_no_tags = re.sub(r"<[^>]+>", "", sub.content)
#         words = text_no_tags.translate(
#             str.maketrans("", "", string.punctuation.replace("'", ""))
#         ).split()
#
#         mispelled = [word for word in checker.unknown(words)]
#
#         if len(mispelled) > 0:
#             print(mispelled)
#             print(f"Line {i}")
#
#             highlighted = sub_track.entries[i - 1].content
#             for w in mispelled:
#                 highlighted = highlighted.replace(
#                     w, f"{FONTCOL.FAIL}{w}{FONTCOL.DEFAULT}"
#                 )
#             print(f"{highlighted}\n")


if __name__ == "__main__":
    main()
