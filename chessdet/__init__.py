# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 12:24:55 2023

@author: shane
"""
import os

from chessdet.env import CHESS_DET_GOOGLE_SHEET_GAMES_GID, CHESS_DET_GOOGLE_SHEET_KEY

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


def _url(gid: int) -> str:
    """Hard-coded URL values pointing to our sheet"""

    return (
        "https://docs.google.com/spreadsheet/ccc"
        f"?key={CHESS_DET_GOOGLE_SHEET_KEY}"
        f"&gid={gid}"
        "&output=csv"
    )


# URL to Google Sheet
CSV_GAMES_URL = _url(CHESS_DET_GOOGLE_SHEET_GAMES_GID)

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
    "Chess960",
    "Atomic",
    "Crazy house",
    "Three check",
    "King of the hill",
    "Racing kings",
    "Horde",
}
