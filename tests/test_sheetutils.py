# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 14:10:51 2023

@author: shane
"""
import os

import pytest
import requests
from requests_mock import Mocker

from chessdet.sheetutils import cache_csv_games_file, get_google_sheet
from tests import TEST_CSV_GAMES_FILE_PATH_FOR_CACHEABLE_TEST

TEST_CSV_GAMES_URL = "https://url"
EMPTY_BYTES = bytes(str(), encoding="utf-8")


def test_get_google_sheet_happy_path(requests_mock: Mocker) -> None:
    """Tests to see if the GET sheet method works"""
    requests_mock.get(TEST_CSV_GAMES_URL, content=EMPTY_BYTES, timeout=3)

    result = get_google_sheet(TEST_CSV_GAMES_URL)
    assert isinstance(result, bytes)
    assert EMPTY_BYTES == result


def test_get_google_sheet_error(requests_mock: Mocker) -> None:
    """Tests to see if the GET sheet method works"""
    requests_mock.get(TEST_CSV_GAMES_URL, status_code=404, timeout=3)

    with pytest.raises(requests.exceptions.HTTPError):
        get_google_sheet(TEST_CSV_GAMES_URL)


def test_cache_csv_games_file() -> None:
    """Test the CSV saving mechanism"""
    cache_csv_games_file(
        EMPTY_BYTES, _file_path=TEST_CSV_GAMES_FILE_PATH_FOR_CACHEABLE_TEST
    )

    assert os.path.isfile(TEST_CSV_GAMES_FILE_PATH_FOR_CACHEABLE_TEST)
    try:
        os.remove(TEST_CSV_GAMES_FILE_PATH_FOR_CACHEABLE_TEST)
    except FileExistsError:
        print(f"WARN: failed to remove '{TEST_CSV_GAMES_FILE_PATH_FOR_CACHEABLE_TEST}'")


if __name__ == "__main__":
    pytest.main()
