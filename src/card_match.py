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
from src.deck import Deck, Ranks
from src.players import CardPlayer


class CardMatch:
    def __init__(self, card_players):
        self.card_players = card_players
        self.deck = Deck()
        self.deck.shuffle()
        for pl in card_players:
            pl.stats.card_games += 1

    def get_winner(self):
        rank_players = sorted(self.card_players, key=lambda x: x.stats.aces, reverse=True)
        if len(rank_players) > 1:
            if rank_players[0].stats.aces == rank_players[1].stats.aces:
                return None
        return rank_players[0] if rank_players else None

    def playing(self, player: CardPlayer):
        if self.deck.has_cards():
            card_picked = self.deck.take_card()
            player.stats.cards.append(card_picked)
            if card_picked.rank == Ranks.ACE:
                player.stats.aces += 1
            return True
        else:
            return False
