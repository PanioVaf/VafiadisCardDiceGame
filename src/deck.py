# Copyright (C) 2020 Vafiadis Panagiotis
#
# Computer Science Department Faculty of Sciences - Campus of Kavala
# International Hellenic University
#
# MPhil in Advanced Technologies in Informatics and Computers
# Advanced Programming and Rich Internet Applications
#
# This is free software and you are welcome to redistribute it
# under certain conditions.

from enum import Enum
from itertools import product
from random import shuffle


class Card(object):
    """Card class"""

    def __init__(self, suit, rank):
        if rank in Ranks and suit in Suits:
            self.rank = rank
            self.suit = suit
        else:
            self.rank = None
            self.suit = None

    def __str__(self):
        return str(self.rank.name) + " " + str(self.suit.name)


class Ranks(Enum):
    """Decks Rank enum"""
    TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN, JACK, QUEEN, KING, ACE = range(2, 15)

    def __str__(self):
        return str(self.value)


class Suits(Enum):
    """Decks Suits enum"""
    CLUBS, DIAMONDS, HEARTS, SPADES = range(1, 5)


class Deck(object):
    """Deck class"""

    def __init__(self):
        self.cards = [Card(suit, rank) for suit, rank in product(Suits, Ranks)]

    def __str__(self):
        return str([str(card) for card in self.cards])

    def has_cards(self):
        return len(self.cards) != 0

    def take_card(self):
        """take card(s) by removing them from deck"""
        return self.cards.pop()

    def shuffle(self):
        """Shuffles deck"""
        shuffle(self.cards)
