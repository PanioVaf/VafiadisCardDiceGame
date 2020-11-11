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

import json
from src.players import CardPlayer, DicePlayer, CardDicePlayer


def load_players(file_name):
    all_players = []
    all_player_ids = set()

    with open(file_name, 'r') as players_file:
        players = json.load(players_file)
        for player in players:
            if '__type__' in player:
                if 'player_id' not in player:
                    raise Exception("Player has no id")
                if player['player_id'] in all_player_ids:
                    raise Exception("Player ids should be unique. Duplicated id = %s" % player['player_id'])
                else:
                    all_player_ids.add(player['player_id'])

                if player['__type__'] == 'CardPlayer':
                    all_players.append(CardPlayer(first_name=player['first_name'],
                                                  last_name=player['last_name'],
                                                  player_id=player['player_id'],
                                                  player_type_desc=player['player_type_desc']))
                elif player['__type__'] == 'DicePlayer':
                    all_players.append(DicePlayer(first_name=player['first_name'],
                                                  last_name=player['last_name'],
                                                  player_id=player['player_id'],
                                                  player_type_desc=player['player_type_desc'],
                                                  dice_prob=player['dice_prob']))
                elif player['__type__'] == 'CardDicePlayer':
                    all_players.append(CardDicePlayer(first_name=player['first_name'],
                                                      last_name=player['last_name'],
                                                      player_id=player['player_id'],
                                                      player_type_desc=player['player_type_desc'],
                                                      dice_prob=player.get('dice_prob', None)))
    return all_players
