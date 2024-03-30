from pathlib import Path
import srt
from spellchecker import SpellChecker


def main():
    test_file = Path("path")
    x = srt.Subtitle(test_file)

    checker = SpellChecker()

    for i, sub in enumerate(x.entries, 1):
        words = sub.content.split()
        mispelled = [word for word in words if checker.unknown(word)]

        if len(mispelled) > 1:
            print(f"{i} -> {mispelled}")


if __name__ == "__main__":
    main()
