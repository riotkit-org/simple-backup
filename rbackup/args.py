"""
Common arguments
"""


import os
from argparse import ArgumentParser


def add_common_args(parser: ArgumentParser):
    """
    Adds common arguments into an ArgumentParser instance
    """

    parser.add_argument(
        "--remote-type", 
        help="Remote type: s3, local", 
        default="local"
    )
    parser.add_argument(
        "--remote", "-r", 
        help="Remote connection string",
        required=os.getenv("REMOTE_CONNECTION_STRING", "") == "",
        default=os.getenv("REMOTE_CONNECTION_STRING", "")
    )
