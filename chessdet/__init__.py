# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 12:24:55 2023

@author: shane
"""
import argparse
import math
import os
import shutil

# Package info
__title__ = "cr"
__version__ = "0.0.1.dev10"
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

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Enums
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Scores & outcomes
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

WHITE = "1-0"
BLACK = "0-1"
DRAW = "1/2-1/2"

ENUM_SCORES = {WHITE, BLACK, DRAW}

ENUM_TERMINATION = {
    # Win / Loss
    "Checkmate",
    "Resignation",
    "Clock flag",
    "Other",
    # Draw
    "Agreement",
    "Repetition",
    "Stalemate",
    "Insufficient material",
    "50 move rule",
}

# Variants
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
STANDARD = "Standard"

VARIANTS = [
    STANDARD,
    "Armageddon",
    "Chess960",
    "Atomic",
    "Crazy house",
    "Three check",
    "King of the hill",
    "Racing kings",
    "Horde",
    "Grand chess",
    # 4 player
    "Head and hand",
    "Bug house",
]
ENUM_VARIANTS = set(VARIANTS)

# Time control
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TIME_CONTROL_ULTRA_BULLET = ("UltraBullet", 30)
TIME_CONTROL_BULLET = ("Bullet", 180)
TIME_CONTROL_BLITZ = ("Blitz", 480)
TIME_CONTROL_RAPID = ("Rapid", 1500)
TIME_CONTROL_CLASSICAL = ("Classical", math.inf)
TIME_CONTROL_CORRESPONDENCE = ("Correspondence", -1)

TIME_CONTROLS = [
    x[0]
    for x in (
        TIME_CONTROL_ULTRA_BULLET,
        TIME_CONTROL_BULLET,
        TIME_CONTROL_BLITZ,
        TIME_CONTROL_RAPID,
        TIME_CONTROL_CLASSICAL,
        # FIXME: Does this break any tests?
        TIME_CONTROL_CORRESPONDENCE,
    )
]
ENUM_TIME_CONTROLS = set(TIME_CONTROLS)


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
