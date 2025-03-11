import os
import logging

from pathlib import Path
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

logging.basicConfig(
    encoding="utf-8",
    level="DEBUG",
    format="%(levelname)s - %(asctime)s | %(message)s",
    filename="/var/log/static_site_bootdev.log",
    filemode="w",
    datefmt="%m/%d/%Y %I:%M:S %P"
)

working_dir = Path(__file__)
source_dir = working_dir.parent.parent.joinpath("static")
target_dir = working_dir.parent.parent.joinpath("public")

def main():
    logging.info("Starting main function.")
    initialize()


def initialize():
    # 1. Delete all contents of destination directory.
    print(os.listdir())
    os.remove(target_dir)
    # 2. Copy all files and subdirectories & nest files

    # 3. Add logging.
    pass


if __name__ == "__main__":
    main()
