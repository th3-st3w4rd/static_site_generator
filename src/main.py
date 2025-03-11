import os
import logging
import shutil

from pathlib import Path
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

logging.basicConfig(
    encoding="utf-8",
    level="DEBUG",
    format="%(levelname)s - %(asctime)s | %(message)s",
    filename="/var/log/static_site_bootdev.log",
    filemode="w",
    datefmt="%m/%d/%Y %I:%M:%S %P"
)

working_dir = Path(__file__)
source_dir = working_dir.parent.parent.joinpath("static")
target_dir = working_dir.parent.parent.joinpath("public")

def main():
    logging.info("Starting main function.")
    initialize()


def initialize():
    logging.info("Starting to initialize project")
    # 1. Delete all contents of destination directory.
    if target_dir.exists():
        shutil.rmtree(target_dir)
        logging.debug(f"Removing {target_dir}.")
    # 2. Copy all files and subdirectories & nest files
    if not target_dir.exists():
        shutil.copytree(source_dir, target_dir)
        logging.debug(f"Copy from source to target location.")
    # 3. Add logging.
    


if __name__ == "__main__":
    main()
