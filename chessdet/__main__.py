# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
"""
Created on Fri Feb 10 12:18:04 2023

@author: shane
"""
import argparse
import time
from typing import List, Union
from urllib.error import HTTPError, URLError

import argcomplete

from chessdet import CLI_CONFIG, __email__, __title__, __url__, __version__
from chessdet.argparser.funcs import parser_func_download, parser_func_rate


def build_arg_parser() -> argparse.ArgumentParser:
    """Adds all subparsers and parsing logic"""

    arg_parser = argparse.ArgumentParser(prog=__title__)
    arg_parser.add_argument(
        "-v",
        action="version",
        version=f"{__title__} version {__version__}",
    )

    arg_parser.add_argument(
        "-d", dest="debug", action="store_true", help="Enable detailed error messages"
    )

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Subparsers
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    subparsers = arg_parser.add_subparsers(title=f"{__title__} subcommands")

    # Download sub-parser
    subparser_download = subparsers.add_parser(
        "fetch", help="Download the latest Sheet from Google"
    )
    subparser_download.set_defaults(func=parser_func_download)

    # Rate sub-parser
    subparser_rate = subparsers.add_parser(
        "rate", help="Process CSV, output ratings or player detail"
    )
    subparser_rate.add_argument(
        "-s",
        dest="skip_dl",
        action="store_true",
        help="Skip sheet download, use cached",
    )
    subparser_rate.add_argument(
        "-m", "--matches", action="store_true", help="include fairest match ups"
    )
    subparser_rate.add_argument(
        "-g", "--graph", action="store_true", help="include rating history charts"
    )
    subparser_rate.set_defaults(func=parser_func_rate)

    return arg_parser


def main(args: Union[None, List[str]] = None) -> int:
    """
    Main method for CLI

    @param args: List[str]
    """

    start_time = time.time()
    arg_parser = build_arg_parser()
    argcomplete.autocomplete(arg_parser)

    def parse_args() -> argparse.Namespace:
        """Returns parsed args"""
        if args is None:
            return arg_parser.parse_args()
        return arg_parser.parse_args(args=args)

    def func(parser: argparse.Namespace) -> tuple:
        """Executes a function for a given argument call to the parser"""
        if hasattr(parser, "func"):
            # Print help for nested commands
            if parser.func.__name__ == "print_help":
                return 0, parser.func()

            # Collect non-default args
            args_dict = dict(vars(parser))
            for expected_arg in ["func", "debug"]:
                args_dict.pop(expected_arg)

            # Run function
            if args_dict:
                # Make sure the parser.func() always returns: Tuple[Int, Any]
                return parser.func(args=parser)  # type: ignore
            return parser.func()  # type: ignore

        # Otherwise print help
        arg_parser.print_help()
        return 0, None

    # Build the parser, set flags
    _parser = parse_args()
    CLI_CONFIG.set_flags(_parser)

    # Try to run the function
    exit_code = 1
    try:
        exit_code, *_results = func(_parser)
    except HTTPError as http_error:
        err_msg = f"{http_error.code}: {repr(http_error)}"
        print("Server response error, try again: " + err_msg)
        if CLI_CONFIG.debug:
            raise
    except URLError as url_error:
        print("Connection error, check your internet: " + repr(url_error.reason))
        if CLI_CONFIG.debug:
            raise
    except Exception as exception:  # pylint: disable=broad-except
        print("Unforeseen error, run with -d for more info: " + repr(exception))
        print(f"You can open an issue here: {__url__}")
        print(f"Or send me an email with the debug output: {__email__}")
        if CLI_CONFIG.debug:
            raise
    finally:
        if CLI_CONFIG.debug:
            exc_time = time.time() - start_time
            print(f"\nExecuted in: {round(exc_time * 1000, 1)} ms")
            print(f"Exit code: {exit_code}")

    return exit_code
