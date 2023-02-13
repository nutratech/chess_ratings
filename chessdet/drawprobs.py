# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 16:27:33 2023

@author: shane
"""
import math

# pylint: disable=invalid-name


def P_white(r1: float, r2: float) -> float:
    """
    Calculate probability that white wins outright. Based on empirical data and
    polynomial approximations.
    NOTE: r1 is white, r2 is black

    https://spp.fide.com/wp-content/uploads/2020/11/2016-probability-of-the-outcome.pdf
    """

    r_avg = (r1 + r2) / 2
    r_delta = r1 - r2

    WLL = -1492 + r_avg * 0.391
    WCL = 40
    WUL = 1691 - r_avg * 0.428

    if r_avg > 1200:
        WCV = 0.45 - 0.1 * (r_avg - 1200) ** 2 / 1200**2
    else:
        WCV = 0.45

    # Main procedure
    if r_delta < WLL:
        return 0.0
    if WLL <= r_delta <= WCL:
        return WCV * (r_delta - WLL) ** 2 / (WCL - WLL) ** 2
    if WCL <= r_delta <= WUL:
        return 1 - (1 - WCV) * (r_delta - WUL) ** 2 / (WCL - WUL) ** 2
    # else r_delta > WUL
    return 1.0


def P_black(r1: float, r2: float) -> float:
    """
    Same, but for black.
    NOTE: r1 is white, r2 is black

    Note that 1 = P_white + P_black + P_draw.
    And we are after P_draw.
    """

    r_avg = (r1 + r2) / 2
    r_delta = r1 - r2

    BLL = -1753 + r_avg * 0.416
    BCL = -80
    BUL = 1428 - r_avg * 0.388

    if r_avg > 1200:
        BCV = 0.46 - 0.13 * (r_avg - 1200) ** 2 / 1200**2
    else:
        BCV = 0.46

    # Main procedure
    if r_delta < BLL:
        return 1.0
    if BLL <= r_delta <= BCL:
        return 1 - (1 - BCV) * (r_delta - BLL) ** 2 / (BCL - BLL) ** 2
    if BCL <= r_delta <= BUL:
        return BCV * (r_delta - BUL) ** 2 / (BCL - BUL) ** 2
    # else r_delta > BUL
    return 0.0


def P_draw(r1: float, r2: float) -> float:
    """
    Calculate draw probability.
    NOTE: r1 is white, r2 is black
    """
    return 1 - P_white(r1, r2) - P_black(r1, r2)


def P_draw_2(r1: float, r2: float) -> float:
    """Calculate draw probability between player1 and player2"""
    r_delta = r1 - r2
    r_avg = (r1 + r2) / 2

    gamma = (
        0.02
        + 0.0000169375 * r1
        + 6.74485 * 10**-9 * r1**2
        + 5.96321 * 10**-11 * r1**3
        - 1.22154 * 10**-14 * r1**4
    )

    std_dev = 200 * math.sqrt(2)
    return gamma / math.cosh( r_delta / std_dev / 1.5)**2
    # return gamma * math.exp(-(r_delta**2) / std_dev**2)
    # return 1/(1-gamma)*(
    #     1
    #     / (math.sqrt(2 * math.pi) * math.e)
    #     * math.exp(-((r_delta / 200) ** 2) / (2 * math.e**2))
    # )
