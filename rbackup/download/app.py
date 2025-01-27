"""
Downloads a remote file and saves to local path
"""

from argparse import ArgumentParser
from logging import info, basicConfig, INFO, DEBUG
from ..filesystem import Filesystem, create_fs
from ..args import add_common_args


class App:
    """
    Main class
    """

    fs: Filesystem

    def __init__(self, fs: Filesystem):
        self.fs = fs

    def download(self, src: str, dest: str = ''):
        """
        Uploads a file to the remote filesystem
        """

        info(f"Downloading '{src}' and saving to '{dest}'")
        self.fs.download(src, dest)

        info("Done")


def add_args(parser: ArgumentParser):
    """
    Configures argparse
    """
    parser.add_argument("src", help="Remote name")
    parser.add_argument("dest", help="Target local path")


def run_from_args(args: dict):
    """
    Runs the application from already parsed args
    """
    app = App(create_fs(args['remote_type'], args['remote']))
    app.download(
        src=args['src'],
        dest=args['dest'],
    )


def main():
    """
    __main__
    """
    parser = ArgumentParser("rbackup.download")
    add_common_args(parser)
    add_args(parser)

    args = vars(parser.parse_args())
    basicConfig(level=DEBUG if args['debug'] else INFO,
                format='%(asctime)s - %(levelname)s :: %(message)s')

    run_from_args(args)
