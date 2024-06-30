from argparse import ArgumentParser
from logging import basicConfig, INFO
from .rotate.app import add_args as add_rotate_args, run_from_args as run_rotate_from_args
from .upload.app import add_args as add_upload_args, run_from_args as run_upload_from_args
from .args import add_common_args


def main():
    """ __main__ """
    basicConfig(level=INFO, format='%(asctime)s - %(levelname)s :: %(message)s')

    parser = ArgumentParser("rbackup-rotate")
    add_common_args(parser)
    add_rotate_args(parser)
    add_upload_args(parser)

    args = vars(parser.parse_args())
    run_rotate_from_args(args)
    run_upload_from_args(args)
    run_rotate_from_args(args)
