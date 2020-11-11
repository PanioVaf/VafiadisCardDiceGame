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

from src.players import DicePlayer


class DiceMatch:
    def __init__(self, player1: DicePlayer, player2: DicePlayer):
        self.DICE_ROLLS = 10
        self.player1 = player1
        self.player2 = player2
        self.num_rolls = 0
        self.dice1 = None
        self.dice2 = None
        player1.stats.dice_games += 1
        player2.stats.dice_games += 1

    def get_current_round(self):
        return self.num_rolls

    def is_finished(self):
        return self.num_rolls == 0

    def playing(self):
        if self.num_rolls >= self.DICE_ROLLS:
            return False
        else:
            self.dice1 = self.player1.roll_dice()
            self.dice2 = self.player2.roll_dice()
            if self.dice1 > self.dice2:
                self.player1.stats.dice_score += 1
            elif self.dice2 > self.dice1:
                self.player2.stats.dice_score += 1
            self.num_rolls += 1
            return True



