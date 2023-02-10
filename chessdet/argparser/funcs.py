# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 13:26:28 2023

@author: shane
"""
from typing import Tuple

from chessdet.sheetutils import cache_csv_games_file, get_google_sheet


def parser_func_download() -> Tuple[int, None]:
    """Default function for download parser"""
    cache_csv_games_file(_csv_bytes_output=get_google_sheet())
    return 0, None


def parser_func_rate() -> Tuple[int, tuple]:
    """Default function for rate parser"""
    print("Not implemented!")
    return 0, (None,)
