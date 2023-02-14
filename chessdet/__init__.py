# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 12:24:55 2023

@author: shane
"""
import argparse
import os
import shutil

# Package info
__title__ = "cr"
__version__ = "0.0.1.dev2"
__author__ = "Shane J"
__email__ = "chown_tee@proton.me"
__license__ = "GPL v3"
__copyright__ = "Copyright 2022-2023 Shane J"
__url__ = "https://github.com/nutratech/chess_ratings"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Other constants
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Global variables
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# Console size, don't print more than it
BUFFER_WD = shutil.get_terminal_size()[0]
BUFFER_HT = shutil.get_terminal_size()[1]

# Location on disk to cache CSV file
CSV_GAMES_FILE_PATH = os.path.join(PROJECT_ROOT, "data", "games.csv")

# Dict

DICT_OUTCOME_TO_SCORE = {
    "White": "1-0",
    "Black": "0-1",
    "Draw": "½-½",
}

# Enum
STANDARD = "Standard"

WHITE = "White"
BLACK = "Black"
DRAW = "Draw"

ENUM_OUTCOMES = {
    # Win / Loss
    "Checkmate",
    "Resignation",
    "Expired time",
    # Draw
    "Agreement",
    "Repetition",
    "Stalemate",
    "Insufficient material",
    "50 move rule",
}

ENUM_VARIANTS = {
    "",  # Standard
    "Standard",
    "Armageddon",
    "Chess960",
    "Atomic",
    "Crazy house",
    "Three check",
    "King of the hill",
    "Racing kings",
    "Horde",
}


################################################################################
# CLI config class (settings & preferences, defaults, and flags)
################################################################################


# pylint: disable=too-few-public-methods,too-many-instance-attributes
class CliConfig:
    """Mutable global store for configuration values"""

    def __init__(self, debug: bool = False) -> None:
        self.debug = debug

    def set_flags(self, args: argparse.Namespace) -> None:
        """
        Sets flags:
          {DEBUG, PAGING}
            from main (after arg parse). Accessible throughout package.
            Must be re-imported globally.
        """

        self.debug = args.debug

        if self.debug:
            print(f"Console size: {BUFFER_HT}h x {BUFFER_WD}w")


# Create the shared instance object
CLI_CONFIG = CliConfig()
