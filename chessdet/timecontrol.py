# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 12:13:36 2023

@author: shane
"""

from chessdet import (
    TIME_CONTROL_BLITZ,
    TIME_CONTROL_BULLET,
    TIME_CONTROL_CLASSICAL,
    TIME_CONTROL_RAPID,
    TIME_CONTROL_ULTRA_BULLET,
)


def game_type(base_time: int, increment: int) -> str:
    """
    Return the type of game based on base time and increment formula.
    (See: https://lichess.org/faq#time-controls)

    :param base_time: Starting time in MINUTES.
    :param increment: Increment in SECONDS.
    """

    game_duration = base_time * 60 + increment * 40

    if game_duration <= TIME_CONTROL_ULTRA_BULLET[1]:
        return TIME_CONTROL_ULTRA_BULLET[0]
    if game_duration <= TIME_CONTROL_BULLET[1]:
        return TIME_CONTROL_BULLET[0]
    if game_duration <= TIME_CONTROL_BLITZ[1]:
        return TIME_CONTROL_BLITZ[0]
    # NOTE: include 20+15 in the lower bound of Classical
    if game_duration < TIME_CONTROL_RAPID[1]:
        return TIME_CONTROL_RAPID[0]
        #  else: game_duration < TIME_CONTROL_CLASSICAL[1]:
    return TIME_CONTROL_CLASSICAL[0]
