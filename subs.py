import os
import time
from pathlib import Path
from lib import Matroska, Subtitle


def main(dir: Path):
    
    movie_path = get_file_by_ext(".mkv", dir)
    # mov = Matroska(movie_path)
    # quick_replace(movie_path)

    quick_replace(dir)


def quick_replace(dir: Path) -> None:
    """
    Given a directory containing ONE and only ONE of each:
        an MKV file
        an SRT file,

        the function will remove all subtitle tracks,
        and reencode the MKV file with the SRT file as
        the only subtitle track

    Parameters:
        dir (str) : Path to directory
    """

    if one_for_one(dir):
        movie_path: Path = Path(get_file_by_ext(".mkv", dir))
        sub_path: Path = Path(get_file_by_ext(".srt", dir))

        print(movie_path)
        print(sub_path)

        movie: Matroska = Matroska(movie_path, sub_path)
        movie.ff_swap_subs(aud_map="0:a:0")

    else:
        print("Directory should contain ONE mkv and ONE srt file.")


def quick_sub_edit(dir: Path) -> None:
    sub_file: Path = Path(get_file_by_ext(".srt", dir))
    this_sub: Subtitle = Subtitle(sub_file)
    this_sub.quick_clean()


def sub_extract(dir: Path):
    z = get_file_by_ext(".mkv", dir)

    mov = Matroska(z)
    mov.ff_extract_subs()


def remove_promo(parent: Path) -> None:
    """
    This function will go through any parent directory...
        get all mkv files,
        extract the subtitles from each,
        remove any subtitle entries with unwanted words,
        and re-encode the mkv file.

    Parameters:
        parent (str) : Path to parent directory
    """

    episode_list: list[Path] = get_files_ext("mkv", parent)
    for episode in episode_list:

        this_ep: Matroska = Matroska(episode)
        
        this_sub: Subtitle = Subtitle(this_ep.ff_extract_subs())
        this_sub.quick_clean()

        this_ep.ff_swap_subs()


def get_file_by_ext(ext: str, path: Path):
            
    return [Path(os.path.join(root, file)) for (root, _, files) in os.walk(path) for file in files if file.endswith(ext)][0]
            

def get_files_ext(ext: str, path: Path) -> list[Path]:
    return [Path(os.path.join(root, file))
            for (root, _, files) in os.walk(path)
            for file in files
            if ext in file]


def one_for_one(dir: Path) -> bool:

    m = get_files_ext(".mkv", dir)
    s = get_files_ext(".srt", dir)

    print(m)
    print(s)

    if len(m) == 1 and len(s) == 1:
        return True
    return False


if __name__ == "__main__":

    movie_test = Path(input("Enter a folder: "))
   

    t1 = time.perf_counter()
    # for m in movie_test:
    #     path = Path(m)
    #     main(path)
    main(movie_test)
    t2 = time.perf_counter()

    # print(f"Completed in {t2-t1} seconds.");
