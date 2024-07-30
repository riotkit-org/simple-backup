"""
Uploads a file into the target filesystem
"""


import pathlib
from argparse import ArgumentParser
from logging import info, basicConfig, INFO
from datetime import datetime
from ..filesystem import Filesystem, create_fs
from ..args import add_common_args


def create_dest_filename(src: str) -> str:
    """
    Generates a filename based on a current timestamp and extension of a source file
    """
    src_path = pathlib.Path(src)
    extension = ".".join(src_path.suffixes)
    return "backup-" + datetime.now().strftime("%m-%d-%Y_%H-%M-%S") + extension


class App:
    """
    Main class
    """

    fs: Filesystem

    def __init__(self, fs: Filesystem):
        self.fs = fs

    def upload(self, src: str, dest: str = ''):
        """
        Uploads a file to the remote filesystem
        """
        if dest.strip() == "":
            dest = create_dest_filename(src)

        info(f"Uploading '{src}' to '{dest}'")
        self.fs.upload(src, dest)

        info("Done")


def add_args(parser: ArgumentParser):
    """
    Configures argparse
    """
    parser.add_argument("src", help="Local file as a source")
    parser.add_argument("dest", help="Destination at the remote path", default="", nargs="?")


def run_from_args(args: dict):
    """
    Runs the application from already parsed args
    """
    app = App(create_fs(args['remote_type'], args['remote']))
    app.upload(
        src=args['src'],
        dest=args['dest'],
    )


def main():
    """
    __main__
    """

    basicConfig(level=INFO, format='%(asctime)s - %(levelname)s :: %(message)s')

    parser = ArgumentParser("rbackup.upload")
    add_common_args(parser)
    add_args(parser)

    args = vars(parser.parse_args())
    run_from_args(args)
