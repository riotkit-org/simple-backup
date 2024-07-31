"""
Rotates backup files on the remote or local filesystem
"""


from argparse import ArgumentParser
from logging import info, basicConfig, INFO
from ..filesystem import Filesystem, create_fs, order_files_by_last_modified, filter_by_pattern
from ..args import add_common_args


class App:
    """ Main class """
    fs: Filesystem

    def __init__(self, fs: Filesystem):
        self.fs = fs

    def rotate(self, max_versions: int, pattern: str):
        """
        Keeps only the last X versions in the remote filesystem
        """

        info("Listing files...")
        total_files = self.fs.list_files()
        info(f"There are {len(total_files)} files in remote filesystem overall")

        matched_files = filter_by_pattern(total_files, pattern)
        info(f"{len(matched_files)} files are managed (matching the pattern '{pattern}')")

        if len(matched_files) > max_versions:
            info(f"There are more than {max_versions} files")
            ordered = order_files_by_last_modified(matched_files)
            oldest = ordered[max_versions:]

            for oldest_entry in oldest:
                info(f"Deleting '{oldest_entry.name}' ({oldest_entry.last_modified})")
                self.fs.delete(oldest_entry.name)

        info("Done")


def add_args(parser: ArgumentParser):
    """ Configures argparse """
    parser.add_argument("--max-versions", "-m", help="How many versions to keep?", required=True)
    parser.add_argument("--pattern", "-p", help="Files pattern whitelist (only on the remote)", 
        default=".*")


def run_from_args(args: dict):
    """ Runs the app from dict as input """
    app = App(create_fs(args['remote_type'], args['remote']))
    app.rotate(
        max_versions=int(args['max_versions']),
        pattern=args['pattern'],
    )


def main():
    """ __main """
    parser = ArgumentParser("rbackup-rotate")
    add_args(parser)
    add_common_args(parser)
    args = vars(parser.parse_args())
    basicConfig(level=DEBUG if args['debug'] else INFO,
                format='%(asctime)s - %(levelname)s :: %(message)s')

    run_from_args(args)
