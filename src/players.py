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

import random
from src.player_stats import PlayerStats


class Player(object):
    def __init__(self, first_name, last_name, player_id, player_type_desc):
        self.first_name = first_name
        self.last_name = last_name
        self.player_id = player_id
        self.player_type_desc = player_type_desc
        self.stats = PlayerStats()

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def name(self):
        return f'{self.last_name}, {self.first_name}'

    def is_card_player(self):
        return False

    def is_dice_player(self):
        return False


class CardPlayer(Player):
    def __init__(self, first_name, last_name, player_id, player_type_desc):
        super().__init__(first_name, last_name, player_id, player_type_desc)

    def is_card_player(self):
        return True


class DicePlayer(Player):
    def __init__(self, first_name, last_name, player_id, player_type_desc, dice_prob=None):
        super().__init__(first_name, last_name, player_id, player_type_desc)
        if dice_prob is None:
            dice_prob = [1, 2, 3, 4, 5, 6]
        if len(dice_prob) != 6:
            raise Exception("Dice probabilities should be 6")
        if not all(map(lambda v: 1 <= v <= 6, dice_prob)):
            raise Exception("Dice probabilities should be 1-6")
        self.dice_prob = dice_prob

    def is_dice_player(self):
        return True

    def roll_dice(self):
        return self.dice_prob[random.randint(1, 6) - 1]


class CardDicePlayer(DicePlayer):
    def __init__(self, first_name, last_name, player_id, player_type_desc, dice_prob=None):
        super().__init__(first_name, last_name, player_id, player_type_desc, dice_prob)

    def is_card_player(self):
        return True

    def is_dice_player(self):
        return True

