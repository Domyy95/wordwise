import argparse
from model import Dictionary
from ui import MainMenu


def run(dictionary_file: str):
    dictionary_manager = Dictionary(dictionary_file)
    app = MainMenu(dictionary_manager)
    print(app.run())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dictionary_file",
        required=True,
        help="Path to the dictionary file",
    )

    args, beam_args = parser.parse_known_args()
    run(args.dictionary_file)
