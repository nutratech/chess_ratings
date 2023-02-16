# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 17:14:19 2023

@author: shane
Loads ENVIRONMENT VARIABLES from file: `.env`
"""
import os

import dotenv

dotenv.load_dotenv(verbose=True)

# Google Sheet constants
CHESS_DET_GOOGLE_SHEET_KEY = os.environ["CHESS_DET_GOOGLE_SHEET_KEY"]
CHESS_DET_GOOGLE_SHEET_GAMES_GID = int(os.environ["CHESS_DET_GOOGLE_SHEET_GAMES_GID"])


def _url(gid: int) -> str:
    """Hard-coded URL values pointing to our sheet"""
    return (
        f"https://docs.google.com/spreadsheets/d/{CHESS_DET_GOOGLE_SHEET_KEY}/export"
        "?format=csv"
        f"&gid={gid}"
    )


# URL to Google Sheet
CSV_GAMES_URL = _url(CHESS_DET_GOOGLE_SHEET_GAMES_GID)
