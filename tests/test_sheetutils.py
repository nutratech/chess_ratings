# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 14:10:51 2023

@author: shane
"""
import csv
import os

import pytest
import requests
from requests_mock import Mocker

from chessdet.sheetutils import build_csv_reader, cache_csv_games_file, get_google_sheet
from tests import TEST_CSV_GAMES_CACHE_FILE_PATH, TEST_CSV_GAMES_FILE_PATH

TEST_CSV_GAMES_URL = "https://url"
EMPTY_BYTES = bytes(str(), encoding="utf-8")


def test_get_google_sheet_happy_path(requests_mock: Mocker) -> None:
    """Tests to see if the GET sheet method works"""
    requests_mock.get(TEST_CSV_GAMES_URL, content=EMPTY_BYTES)

    result = get_google_sheet(TEST_CSV_GAMES_URL)
    assert isinstance(result, bytes)
    assert EMPTY_BYTES == result


def test_get_google_sheet_error(requests_mock: Mocker) -> None:
    """Tests to see if the GET sheet method works"""
    requests_mock.get(TEST_CSV_GAMES_URL, status_code=404)

    with pytest.raises(requests.exceptions.HTTPError):
        get_google_sheet(TEST_CSV_GAMES_URL)


def test_cache_csv_games_file() -> None:
    """Test the CSV saving mechanism"""
    cache_csv_games_file(EMPTY_BYTES, _file_path=TEST_CSV_GAMES_CACHE_FILE_PATH)

    assert os.path.isfile(TEST_CSV_GAMES_CACHE_FILE_PATH)
    try:
        os.remove(TEST_CSV_GAMES_CACHE_FILE_PATH)
    except FileExistsError:
        print(f"WARN: failed to remove '{TEST_CSV_GAMES_CACHE_FILE_PATH}'")


EXPECTED_FIELD_NAMES = [
    "date",
    "white",
    "black",
    "result",
    "outcome",
    "location",
    "time",
    "# of moves",
    "opening",
    "variant",
    "notes",
]


def test_build_csv_reader(requests_mock: Mocker) -> None:
    """Test the CSV DictReader builder method with filesystem CSV (cache)"""
    with open(TEST_CSV_GAMES_FILE_PATH, "rb") as _f:
        file_content = _f.read()

    # Mock the Google Sheet call with the test CSV data in bytes() form
    requests_mock.get(TEST_CSV_GAMES_URL, content=file_content)
    reader = build_csv_reader(TEST_CSV_GAMES_URL, TEST_CSV_GAMES_FILE_PATH)

    assert isinstance(reader, csv.DictReader)
    assert reader.fieldnames == EXPECTED_FIELD_NAMES


def test_build_csv_reader_cache_fallback(requests_mock: Mocker) -> None:
    """Test the CSV DictReader builder method with filesystem CSV (cache)"""
    # Mock the failure call to fall back to CSV on filesystem
    requests_mock.get(TEST_CSV_GAMES_URL, status_code=404)
    reader = build_csv_reader(TEST_CSV_GAMES_URL, TEST_CSV_GAMES_FILE_PATH)

    assert isinstance(reader, csv.DictReader)
    assert reader.fieldnames == EXPECTED_FIELD_NAMES


if __name__ == "__main__":
    pytest.main()
