# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 21:06:08 2023

@author: shane
"""
from typing import List, Tuple

import matplotlib.pyplot as plt
import pytest

from chessdet.drawprobs import P_black, P_draw, P_white

# pylint: disable=invalid-name


# BASE_RATING = 1500


def _range_domain(mode: str, base_rating: int) -> Tuple[List[int], List[float]]:
    r1 = base_rating
    _range = list(range(r1 - 700, r1 + 700, 10))
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


@pytest.mark.parametrize("base_rating", [300, 900, 1500, 2100, 2700])
def test_P_draw(base_rating: int) -> None:
    """Test P(draw) function"""
    assert P_white(base_rating, base_rating) < 0.5
    assert P_black(base_rating, base_rating) < 0.5
    assert P_draw(base_rating, base_rating) > 0.0

    _range_white, _domain_white = _range_domain(mode="white", base_rating=base_rating)
    _range_black, _domain_black = _range_domain(mode="black", base_rating=base_rating)
    _range_draw, _domain_draw = _range_domain(mode="draw", base_rating=base_rating)

    # plot
    _, ax = plt.subplots()
    ax.scatter(_range_white, _domain_white)
    ax.scatter(_range_black, _domain_black)
    ax.scatter(_range_draw, _domain_draw)
    plt.show()
