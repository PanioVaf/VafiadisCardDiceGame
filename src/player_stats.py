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


class PlayerStats(object):
    def __init__(self):
        self.dice_score = 0
        self.aces = 0
        self.cards = []
        self.card_games = 0
        self.dice_games = 0
