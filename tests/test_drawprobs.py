# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 21:06:08 2023

@author: shane
"""
from typing import List, Tuple

import matplotlib.pyplot as plt

from chessdet.drawprobs import P_black, P_draw, P_white

# pylint: disable=invalid-name


BASE_RATING = 1500


def _range_domain(mode: str) -> Tuple[List[int], List[float]]:
    r1 = BASE_RATING
    _range = list(range(BASE_RATING - 700, BASE_RATING + 700, 10))
    _domain = []
    for r2 in _range:
        _domain_dict = {
            "white": P_white(r1, r2),
            "black": P_black(r1, r2),
            "draw": P_draw(r1, r2),
        }
        y = _domain_dict[mode]
        _domain.append(y)

    return _range, _domain


def test_P_draw() -> None:
    """Test P(draw) function"""
    assert P_white(BASE_RATING, BASE_RATING) < 0.5
    assert P_black(BASE_RATING, BASE_RATING) < 0.5
    assert P_draw(BASE_RATING, BASE_RATING) > 0.0

    _range_white, _domain_white = _range_domain(mode="white")
    _range_black, _domain_black = _range_domain(mode="black")
    _range_draw, _domain_draw = _range_domain(mode="draw")

    # plot
    _, ax = plt.subplots()
    ax.scatter(_range_white, _domain_white)
    ax.scatter(_range_black, _domain_black)
    ax.scatter(_range_draw, _domain_draw)
    plt.show()
