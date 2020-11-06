# Copyright (C) 2019  - Vafiadis Panagiotis
# Computer Science Department
# Faculty of Sciences - Campus of Kavala
# International Hellenic University
# MPhil in Advanced Technologies in Informatics and Computers
# Advanced Programming and Rich Internet Applications
# This is free software and you are welcome to redistribute it
# under certain conditions.
import itertools
import random
import operator
import json
import time
import os
import sys
import numpy

from collections import OrderedDict
from numpy import random
from enum import Enum
from itertools import product
from random import shuffle
from classes.player_types import PlayerTypes

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

# Final Objects Initialized
DICE_ROLLS = 10
CARD_PLAYERS = [1, 3, 6, 7]
DICE_PLAYERS = [2, 3, 4, 5, 6, 7]
DISPLAY_WIDTH = 1500
DISPLAY_HEIGHT = 750

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
LGREEN = (40, 120, 80)
RED = (130, 10, 0)
GREEN = (0, 255, 0)
DGREEN = (0, 155, 0)
selected_card_y_pos_player_1 = 330
selected_card_y_pos_player_2 = 230
FONT_SIZE = 17
delay_time_ms = 1000
number_of_cards = 10
turn_count = 1

PATH = os.path.abspath((os.path.join(os.pardir)))

# Initialize game, set the screen and background
pygame.init()
my_font = pygame.font.SysFont('Times New Roman', FONT_SIZE, True)
bg_surf = pygame.image.load(PATH + '/resource/table.jpg')
bg_surf = pygame.transform.scale(bg_surf, (DISPLAY_WIDTH - 300, DISPLAY_HEIGHT))
bg_logo = pygame.image.load(PATH + '/resource/ihu.png')
screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
joker = pygame.image.load(PATH + "/resource/joker.jpg")
joker = pygame.transform.scale(joker, (DISPLAY_WIDTH - 1400, DISPLAY_HEIGHT - 670))
pygame.display.set_caption("Welcome to John's Card Dice Game, powered by Panagiotis Vafiadis")
clock = pygame.time.Clock()

player_pic = pygame.image.load(PATH + "/resource/player.png")
player_pic = pygame.transform.scale(player_pic, (110, 110))


# Enum classes
class Ranks(Enum):
    TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN, JACK, QUEEN, KING, ACE = range(2, 15)


class Suits(Enum):
    CLUBS, DIAMONDS, HEARTS, SPADES = range(1, 5)


# main classes
class Card(object):
    """Card object represents a standard playing card.

    The object attributes, suit and rank, are implemented as enums whose values determine the weight of the card
    """

    def __init__(self, suit, rank, in_deck=False, image=None):
        if rank in Ranks and suit in Suits:
            self.rank = rank
            self.suit = suit
        else:
            self.rank = None
            self.suit = None

        self.in_deck = in_deck
        self.image = image
        self.position_x, self.position_y = 0, 0
        self.horizontal_dimension = None
        self.vertical_dimension = None

    def __str__(self):
        return str(self.rank.name) + " " + str(self.suit.name)

    def __eq__(self, other):
        return True if self.rank == other.rank and self.suit == other.suit else False

    def __gt__(self, other):
        """Tests suit precedence, if suits are equal then checks ranks precedence"""
        if self.suit == other.suit:
            if self.rank.value > other.rank.value:
                return True
        if self.suit.value > other.suit.value:
            return True

        return False


class Deck(object):
    """A deck is a collection of 52 Card objects

    Object attributes: cards, removed
    methods: draw(range = 1), deck_shuffle()
    """

    def __init__(self):
        self.cards = [Card(suit, rank, in_deck=True) for suit, rank in product(Suits, Ranks)]
        self.removed = []

    def __str__(self):
        return str([str(card) for card in self.cards])

    def draw(self, range_is=1):
        """Draw card(s) by removing them from deck"""
        drawn_cards = self.cards[:range_is]
        for card in drawn_cards:
            card.in_deck = False
        del self.cards[:range_is]
        self.removed.append(drawn_cards)
        return drawn_cards

    def deck_shuffle(self):
        """Shuffles deck"""
        shuffle(self.cards)


class Player(object):
    """Implementation of a player object

    Object attributes: name, hand, score, turn, card_selected
    methods: remove_from_hand(card)
    """

    def __init__(self, name, hand=None, score=0, turn_is=False):
        self.name = name
        self.hand = hand
        self.score = score
        self.turn = turn_is
        self.selected_card = None

    def __str__(self):
        return str(self.name)

    def remove_from_hand(self, card):
        """Removes a card object from the players hand"""
        if card and card in self.hand:
            position = self.hand.index(card)
            del self.hand[position]
            return card
        return None


# Functions
def get_dice_images():
    """Load dice images"""
    dices = {}
    for i in range(1, 7):
        dices[i] = pygame.image.load(PATH + ("/resource/dice/%s.png" % str(i)))
    return dices


dice_imag = get_dice_images()


def show_hand(player):
    """Displays all cards in hand of player on pygame display object"""
    x, y, space_between_cards = 5, 462, 5
    for card in player.hand:
        card.position_x, card.position_y = x, y
        screen.blit(card.image, (x, y))
        x += card.horizontal_demension + space_between_cards


def select_card(player, mouse_x, mouse_y):
    """Player selects a card to play"""
    if mouse_x:
        for card in player.hand:
            lower_x, upper_x = (card.position_x, card.position_x + card.horizontal_demension)
            lower_y, upper_y = (card.position_y, card.position_y + card.vertical_demension)

            if lower_x < mouse_x < upper_x:
                if lower_y < mouse_y < upper_y:
                    player.selected_card = card


def load_card(card):
    """Load card images"""
    card.image = pygame.image.load(PATH + '/resource/cards/' + card + '.png')
    width, height = card.image.get_size()
    card.horizontal_dimension = width
    card.vertical_dimension = height


def play_selected_card(player):
    """Display card that is selected on pygame display object"""
    x = player.selected_card.position_x = 220
    y = player.selected_card.position_y
    screen.blit(player.selected_card.image, (x, y))


def show_winner(players):
    """Display text stating game winner at end of game"""
    counter = 1
    lane_c = 15
    screen_background(bg_surf, bg_logo)
    score_label = my_font.render("P SCORE    NAME", False, BLACK)
    screen.blit(score_label, (0, 0))
    rank_players = OrderedDict(sorted(players.items(), key=lambda kv: kv[1]["score"]["dice_score"], reverse=True))
    for player, value in rank_players.items():
        score_val = value["score"]["dice_score"]
        print(score_val)
        if score_val == 0:
            continue

        full_name = value["name"]["first_name"] + " " + value["name"]["last_name"]
        player_score = my_font.render("%s.   %s       %s" % (str(counter), str(score_val), full_name), False, BLACK)
        screen.blit(player_score, (0, lane_c))
        lane_c += 20
        counter += 1


def show_player_scores(players, game_of_dice=False):
    """Left corner shows the player list"""
    lane_c = 0
    for player in players:
        player_names = my_font.render(" %s. %s is a %s" %
                                      (players[player]["player_num"],
                                       players[player]["name"]["first_name"],
                                       players[player]["player_type_desc"]), False, (0, 0, 0))
        if not game_of_dice:
            player_score = my_font.render(" Card: %s   Dice %s   Ace" % (" " * 8, " " * 8), False, (0, 0, 0))
            player_score_col = my_font.render("%s%s%s%s%s%s" % (" " * 8, players[player]["score"]["card_score"],
                                                                " " * 20, players[player]["score"]["dice_score"],
                                                                " " * 20, players[player]["score"]["aces"]), False, RED)
        else:
            player_score = my_font.render("Dice score: ", False, (0, 0, 0))
            player_score_col = my_font.render("%s%s" % (" " * 20, players[player]["score"]["dice_score"]), False, RED)
        screen.blit(player_names, (0, lane_c))
        screen.blit(player_score, (30, lane_c + FONT_SIZE + 5))
        screen.blit(player_score_col, (50, lane_c + FONT_SIZE + 5))
        lane_c += (FONT_SIZE * 2.8)


def dice_roll(pl):
    if pl["player_type_enum"] in [PlayerTypes.TWO_5_DICE_PLAYER.value,
                                  PlayerTypes.TWO_5_DICE_CARD_PLAYER.value]:
        roll = numpy.argmax(random.multinomial(n=1, pvals=[1 / 6, 1 / 6, 0, 1 / 6, 1 / 3, 1 / 6])) + 1
    elif pl["player_type_enum"] in [PlayerTypes.TWO_6_DICE_CARD_PLAYER.value,
                                    PlayerTypes.TWO_6_DICE_PLAYER.value]:
        roll = numpy.argmax(random.multinomial(n=1, pvals=[1 / 6, 1 / 6, 1 / 6, 1 / 6, 0, 1 / 3])) + 1
    else:
        roll = random.randint(1, 6)
    return roll


def dice_game(players, pl1, pl2):
    pl1['games']['dice_games'] += 1
    pl2['games']['dice_games'] += 1
    for counter in range(1, DICE_ROLLS + 1):
        screen_background(bg_surf, bg_logo)
        show_player_scores(players, True)
        pl_label = my_font.render("%s. %s%sVS%s%s. %s" % (str(pl1['player_num']),
                                                          pl1['name']['first_name'], " " * 8, " " * 8,
                                                          str(pl2['player_num']),
                                                          pl2['name']['first_name']), False, (40, 40, 40))
        round_label = my_font.render("Round %s" % str(counter), False, (40, 40, 40))
        screen.blit(pl_label, (800, 200))
        screen.blit(player_pic, (450, 380))
        screen.blit(player_pic, (1250, 380))
        screen.blit(round_label, (860, 250))
        roll_pl1 = dice_roll(pl1)
        roll_pl2 = dice_roll(pl2)

        if roll_pl1 > roll_pl2:
            for k, v in players.items():
                if v["player_num"] == pl1["player_num"]:
                    v["score"]["dice_score"] += roll_pl1
        if roll_pl1 < roll_pl2:
            for k, v in players.items():
                if v["player_num"] == pl2["player_num"]:
                    v["score"]["dice_score"] += roll_pl2
        screen.blit(dice_imag[roll_pl1], (600, 400))
        screen.blit(dice_imag[roll_pl2], (1100, 400))

        pygame.display.flip()
        # time.sleep(0.1)    # UNCOMMENT and manipulate the value for viewing the game


def meet_by_two(players, cpl_list, pl1, pl2):
    """Players meet by two"""
    # Filtering for only meeting once
    if pl1["player_num"] in pl2["games"]["players_played"] or pl2["player_num"] in pl1["games"]["players_played"]:
        return cpl_list
    pl1["games"]["players_played"].append(pl2["player_num"])
    pl2["games"]["players_played"].append(pl1["player_num"])

    if pl1["player_type_enum"] in CARD_PLAYERS:
        cpl_list.append(pl1["player_num"])
    if pl2["player_type_enum"] in CARD_PLAYERS:
        cpl_list.append(pl2["player_num"])
    if pl1["player_type_enum"] in DICE_PLAYERS and pl2["player_type_enum"] in DICE_PLAYERS:
        dice_game(players, pl1, pl2)
    return cpl_list


def meeting(players):
    """All players meet and classify"""
    card_players = []
    for pl1, pl2 in list(itertools.product(players, players)):
        if pl1 == pl2:
            continue
        meet_by_two(players, card_players, players[pl1], players[pl2])
    return list(set(card_players))


def get_players():
    """"Load all players from file"""
    try:
        with open(PATH + '/resource/players.json', 'r') as players_file:
            players_dict = json.load(players_file)
            players_file.close()
            return players_dict
    except Exception as exc:
        print("error" + str(exc))


def screen_background(image, logo):
    screen.fill(LGREEN)
    pygame.font.init()
    screen.blit(image, (300, 0))
    screen.blit(logo, (660, -50))


def card_game(players, card_players):
    screen_background(bg_surf, bg_logo)
    if not card_players:
        no_pl_label = my_font.render("There are no Card Players... Restart the game", False, (40, 40, 40))
        screen.blit(no_pl_label, (700, 300))
    else:
        deck = Deck()
        deck.deck_shuffle()
        show_player_scores(players, False)
        wid = DISPLAY_WIDTH / len(card_players)
        hei = DISPLAY_HEIGHT / len(card_players)
        for pl in card_players:
            screen.blit(player_pic, (wid + pl * 10, hei))


def main():
    """ Main program function. """
    # Get the Dict with the players
    card_player_list = []
    players_list = get_players()
    pygame.display.flip()
    screen_background(bg_surf, bg_logo)
    label = my_font.render("Press SPACE to START the DICE game!", False, (40, 40, 40))
    screen.blit(label, (770, 300))

    # Game Loop
    game_running = True
    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
                quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    screen_background(bg_surf, bg_logo)
                    show_player_scores(players_list)
                    card_player_list = meeting(players_list)
                    show_winner(players_list)
                    label = my_font.render("Press Joker to continue to CARDS game!", False, (40, 40, 40))
                    screen.blit(label, (750, 400))
                    screen.blit(joker, (860, 500))
            # if event.type == pygame.KEYDOWN:
            #     card_game(players_list, card_player_list)

        pygame.display.update()
        clock.tick(120)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
