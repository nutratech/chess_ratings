# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 15:23:06 2023

@author: shane
"""
import csv
import time
from io import StringIO

import requests

from chessdet import CSV_GAMES_FILE_PATH, CSV_GAMES_URL


def get_google_sheet(url: str = CSV_GAMES_URL) -> bytes:
    """
    Returns a byte array (string) of the Google Sheet in CSV format
    """
    print(f"GET {url}")

    response = requests.get(url, timeout=2)
    response.raise_for_status()

    return bytes(response.content)


def cache_csv_games_file(
    _csv_bytes_output: bytes,
    _file_path: str = CSV_GAMES_FILE_PATH,
) -> None:
    """
    Persists the CSV file into the git commit history.
    Fall back calculation in case sheets.google.com is unreachable.
    (Manually) verify no nefarious edits are made.
    """
    print(f"save to: {_file_path}")
    with open(_file_path, "wb") as _file:
        _file.write(_csv_bytes_output)


def build_csv_reader(
    csv_games_url: str = CSV_GAMES_URL, csv_file_path: str = CSV_GAMES_FILE_PATH
) -> csv.DictReader:
    """Returns a csv.reader() object"""
    t_start = time.time()

    try:
        _csv_bytes_output = get_google_sheet(csv_games_url)
        _csv_file = StringIO(_csv_bytes_output.decode())
        cache_csv_games_file(_csv_bytes_output, csv_file_path)

        reader = csv.DictReader(_csv_file)
        reader.fieldnames = [field.strip().lower() for field in reader.fieldnames or []]

    except (
        requests.exceptions.ConnectionError,
        requests.exceptions.ReadTimeout,
        requests.exceptions.HTTPError,
    ) as err:
        print(repr(err))
        print()
        print("WARN: failed to fetch Google sheet, falling back to cached CSV files...")

        with open(csv_file_path, encoding="utf-8") as _f:
            reader = csv.DictReader(_f)
            reader.fieldnames = [
                field.strip().lower() for field in reader.fieldnames or []
            ]

    t_delta = time.time() - t_start
    print(f"Cached games CSV file in {round(t_delta * 1000, 1)} ms")
    return reader
