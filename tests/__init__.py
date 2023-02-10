# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 14:38:16 2023

@author: shane
"""
import os.path

TEST_ROOT = os.path.realpath(os.path.dirname(__file__))

TEST_CSV_GAMES_FILE_PATH = os.path.join(TEST_ROOT, "data", "games.csv")
TEST_CSV_GAMES_FILE_PATH_FOR_CACHEABLE_TEST = os.path.join(
    TEST_ROOT, "data", "games_cache.csv"
)
