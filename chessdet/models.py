# -*- coding: utf-8 -*-
"""
Created on Sun 08 Jan 2023 11∶26∶34 PM EST

@author: shane
Game model used for players, location, date, outcome, etc.
Player model used for singles & doubles ratings, username, wins/losses, etc.
Club model used for grouping games and players to location names.
"""
import math
from datetime import datetime
from typing import Dict, List, Set, Union

import asciichartpy  # pylint: disable=import-error

from chessdet import (
    CLI_CONFIG,
    DEVIATION_PROVISIONAL,
    ENUM_SCORES,
    ENUM_TERMINATION,
    ENUM_VARIANTS,
    STANDARD,
    TIME_CONTROL_CLASSICAL,
    TIME_CONTROL_CORRESPONDENCE,
    timecontrol,
)
from chessdet.glicko2 import glicko2

CLUB_DICT = {
    "Royal Oak (ROFUM)": "Royal Oak",
    "Oakland County (Methodist Church, Waterford)": "Oakland County",
    "Oak Park (Community Center)": "Oak Park",
    "Port Huron (Palmer Park Rec Center)": "Port Huron",
    "Dearborn Brewing Chess Club": "Dearborn Brew",
    # Other locations (non-clubs)
    "Norm's": "Norm's",
}


# pylint: disable=too-few-public-methods


class Club:
    """
    Model for storing the club name
    """

    def __init__(self, name: str) -> None:
        self.name = CLUB_DICT[name]

        # Other values populated bi-directionally
        self.games = []  # type: ignore
        self.players = []  # type: ignore

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other) -> bool:  # type: ignore
        return bool(self.name == other.name)

    def __hash__(self) -> int:
        return hash(self.name)


class Game:
    """
    Model for storing date, location, wins/losses, opponent, etc.
    TODO:
        - Easily queryable,
            e.g. find max(best_win_opponent_ratings) or avg(opponent_ratings)
        - Decide on life cycle flow of overall app: interface, modularity, & persistence
        - FIXME: Filter based on other VARIANTS. We foolishly aggregate all types today
        - FIXME: use timecontrol.py: calculate different ratings: blitz/rapid/classical
    """

    def __init__(self, row: Dict[str, str]) -> None:
        self.date = datetime.strptime(row["Date"], "%Y-%m-%d")

        self.username_white = row["White"]
        self.username_black = row["Black"]

        self.score = row["Score"]
        self.termination = row["Termination"]

        self.location = Club(row["Location"])

        # Compute time control
        self.time_control = row["Time"]
        self.base_time, self.increment = -1, -1
        self.days_per_move = -1
        self.category = str()
        self.parse_time_control()

        # Optional fields
        self.variant = row["Variant"] or STANDARD
        self.num_moves = int(row["# moves"].split("?")[0] or -1)
        self.opening = row["Opening"]
        self.url_analysis = row["Analysis"]
        self.notes = row["Notes"]

        if CLI_CONFIG.debug:
            print(self)

        # Validation
        self.validate_fields()

    def __str__(self) -> str:
        return (
            f"{self.date.date()} [{self.category}] "
            f"{self.score} "
            f"{self.username_white} vs. {self.username_black}"
        )

    def parse_time_control(self) -> None:
        """Decide base_time and increment, or correspondence time length"""

        if "+" in self.time_control:
            self.base_time = int(self.time_control.split("+")[0])
            self.increment = int(self.time_control.split("+")[1])
            # Assign category
            self.category = timecontrol.game_type(self.base_time, self.increment)
        elif "d" in self.time_control:
            self.days_per_move = int(self.time_control.split("d")[0])
            self.category = TIME_CONTROL_CORRESPONDENCE[0]
        elif float(self.time_control) == math.inf:
            self.base_time = 30
            self.increment = 20
            self.category = TIME_CONTROL_CLASSICAL[0]
        else:
            self.validation_error(
                f"Invalid time control, must contain '+' or 'd', "
                f"got: '{self.time_control}'"
            )

    def validation_error(self, err_msg: str) -> None:
        """Raises a value error with err_msg and printing out the Game().__str__"""
        raise ValueError(f"{err_msg}\nGame: {self}")

    def validate_username(self, username: str) -> None:
        """Verify a username is at least 3 characters long"""
        min_length = 3
        if len(username) < min_length:
            self.validation_error(
                f"Username must be at least {min_length} characters, got: {username}\n"
            )

    def validate_fields(self) -> None:
        """Validates fields to make sure CSV row is properly formatted"""
        self.validate_username(self.username_white)
        self.validate_username(self.username_black)

        # Game score
        if self.score not in ENUM_SCORES:
            self.validation_error(
                f"Invalid score: '{self.score}', must be in {ENUM_SCORES}"
            )

        # Game outcomes
        if self.termination not in ENUM_TERMINATION:
            self.validation_error(
                f"Invalid outcome: '{self.termination}', must be in {ENUM_TERMINATION}"
            )

        # Variant
        if self.variant not in ENUM_VARIANTS:
            self.validation_error(
                f"Invalid variant: '{self.variant}', must be in {ENUM_VARIANTS}"
            )


class Player:
    """
    Model for storing username, rating

    TODO:
        - Include points in scoreboard? Track avg(points) of player1 vs. player2?
        - self.first_game (or self.join_date?)
    """

    def __init__(self, username: str) -> None:
        self.username = username

        # NOTE: length of this is one longer than other arrays
        self.ratings = [glicko2.Rating()]

        self.opponent_ratings: Dict[str, List[glicko2.Rating]] = {
            "wins": [],
            "losses": [],
            "draws": [],
        }

        # NOTE: separate scripts doubles & singles, it would aggregate both (is okay?)
        # Used to decide home club
        self.club_appearances: Dict[str, int] = {}

        # WIP section
        self.games: List[Game] = []

    def __str__(self) -> str:
        # NOTE: return this as a tuple, and tabulate it (rather than format as string)?
        return f"{self.username} [{self.str_rating()}]"

    @property
    def rating(self) -> glicko2.Rating:
        """Gets the rating"""
        # FIXME: a lot of these properties would need to support variant != "STANDARD"
        # TODO: add support for separate rating_white and rating_black properties
        glicko = glicko2.Glicko2()
        _rating = self.ratings[-1]

        return glicko.create_rating(mu=_rating.mu, phi=_rating.phi, sigma=_rating.sigma)

    def rating_max(self) -> Union[None, int]:
        """Personal best, ignore highly uncertain ratings"""
        filtered_ratings = filter(lambda y: y.phi < DEVIATION_PROVISIONAL, self.ratings)
        try:
            return round(max(x.mu for x in filtered_ratings))
        except ValueError:
            return None

    def add_club(self, club: str) -> None:
        """Adds a club tally to the club appearances dictionary"""

        if club in self.club_appearances:
            self.club_appearances[club] += 1
        else:
            self.club_appearances[club] = 1

    def home_club(self) -> str:
        """Gets the most frequent place of playing"""
        return max(
            self.club_appearances,
            key=self.club_appearances.get,  # type: ignore
        )

    def clubs(self) -> List[str]:
        """
        Gets all the clubs someone has appeared at
        TODO: sort alphabetically or by frequency of appearance (most frequented club)
        """
        _clubs: Set[str] = set()
        _clubs.update(self.club_appearances)
        return sorted(list(_clubs))

    def str_rating(self) -> str:
        """Returns a friendly string for a rating, e.g. 1500 ± 300"""
        _rating = self.rating
        _mu = round(_rating.mu)
        _196_phi = int(round(_rating.phi * 1.96, -1))  # Round to 10s

        return f"{_mu} ± {_196_phi}"

    def str_wins_draws_losses(self) -> str:
        """Returns e.g. 5-2"""

        n_wins = len(self.opponent_ratings["wins"])
        n_draws = len(self.opponent_ratings["draws"])
        n_losses = len(self.opponent_ratings["losses"])

        return f"+{n_wins} ={n_draws} -{n_losses}"

    def avg_opponent(self) -> int:
        """Returns average opponent"""

        # FIXME: filter if < DEVIATION_PROVISIONAL
        _avg_opponent = sum(
            sum(x.mu for x in self.opponent_ratings[_result])
            for _result in ["wins", "losses", "draws"]
        ) / (
            sum(
                len(self.opponent_ratings[_result])
                for _result in ["wins", "losses", "draws"]
            )
        )
        return round(_avg_opponent)

    def best_result(self, mode: str = "wins") -> Union[None, int]:
        """Returns best win"""
        try:
            return round(
                max(
                    x.mu
                    for x in self.opponent_ratings[mode]
                    if x.phi < DEVIATION_PROVISIONAL
                )
            )
        except (ValueError, TypeError):
            return None

    def graph_ratings(
        self, graph_width_limit: int = 50, graph_height: int = 12
    ) -> List[int]:
        """
        Prints an ASCII graph of rating over past 50 games
        """

        _series = [round(x.mu) for x in self.ratings[-graph_width_limit:]]
        _plot = asciichartpy.plot(_series, {"height": graph_height})
        print(_plot)
        return _series
