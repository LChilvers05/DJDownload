import argparse
from data.repository import Repository
import slicer.app as slicer
import playlist_prep.app as playlist_prep

def main(args):
    repo = Repository()

    if args.prepare_playlists:
        playlist_prep.App(repo).run()
    else:
        slicer.App(repo).run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Slice playlist audio or prepare playlists for recording.")
    parser.add_argument(
        "-p",
        "--prepare-playlists",
        action="store_true",
        help="prepare playlists by inserting silence between tracks",
    )
    args = parser.parse_args()
    main(args)
