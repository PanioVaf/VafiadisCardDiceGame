# Copyright (C) 2019  - Vafiadis Panagiotis
# Computer Science Department
# Faculty of Sciences - Campus of Kavala
# International Hellenic University
# MPhil in Advanced Technologies in Informatics and Computers
# Advanced Programming and Rich Internet Applications
# This is free software and you are welcome to redistribute it
# under certain conditions.
import itertools
import json
import os
import random
import sys
import numpy
import time

from collections import OrderedDict
from enum import Enum, IntEnum
from itertools import product
from random import shuffle
from numpy import random

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
GREEN = (40, 120, 80)
RED = (130, 10, 0)
LGREEN = (130, 200, 150)
FONT_SIZE = 17

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
pygame.display.set_caption("Welcome to John's Card Dice Game, developed by Panagiotis Vafiadis")
clock = pygame.time.Clock()

player_pic = pygame.image.load(PATH + "/resource/player.png")
player_pic = pygame.transform.scale(player_pic, (110, 110))


# Enum classes
class Ranks(Enum):
    """Decks Rank enum"""
    TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN, JACK, QUEEN, KING, ACE = range(2, 15)


class Suits(Enum):
    """Decks Suits enum"""
    CLUBS, DIAMONDS, HEARTS, SPADES = range(1, 5)


class PlayerTypes(IntEnum):
    """Player types enum"""
    CARD_PLAYER, DICE_PLAYER, CARD_DICE_PLAYER, TWO_5_DICE_PLAYER, \
        TWO_6_DICE_PLAYER, TWO_5_DICE_CARD_PLAYER, TWO_6_DICE_CARD_PLAYER = range(1, 8)


# main classes
class Card(object):
    """Card class"""

    def __init__(self, suit, rank, in_deck=False, image=None):
        if rank in Ranks and suit in Suits:
            self.rank = rank
            self.suit = suit
        else:
            self.rank = None
            self.suit = None

        self.in_deck = in_deck

    def __str__(self):
        return str(self.rank.name) + " " + str(self.suit.name)


class Deck(object):
    """Deck class"""

    def __init__(self):
        self.cards = [Card(suit, rank, in_deck=True) for suit, rank in product(Suits, Ranks)]
        self.removed = []

    def __str__(self):
        return str([str(card) for card in self.cards])

    def draw(self):
        """Draw card(s) by removing them from deck"""
        drawn_cards = self.cards.pop()
        self.removed.append(drawn_cards)
        return drawn_cards

    def deck_shuffle(self):
        """Shuffles deck"""
        shuffle(self.cards)


class Player:
    def __init__(self, name,
                 player_num,
                 player_type_enum,
                 player_type_desc,
                 score,
                 games):
        self.name = name
        self.player_num = player_num
        self.player_type_enum = player_type_enum
        self.player_type_desc = player_type_desc
        self.score = score
        self.games = games


class Games:
    def __init__(self, card_games, dice_games, players_played):
        self.card_games = card_games
        self.dice_games = dice_games
        self.players_played = players_played


class Score:
    def __init__(self, card_score, dice_score, aces, cards):
        self.card_score = card_score
        self.dice_score = dice_score
        self.aces = aces
        self.cards = cards


class Name:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def name(self):
        return f'{self.last_name}, {self.first_name}'


# Functions for the layout of the game
def screen_background(image, logo):
    screen.fill(GREEN)
    pygame.font.init()
    screen.blit(image, (300, 0))
    screen.blit(logo, (660, -50))


# Functions for getting items from resources dir
def get_dice_images():
    """Load dice images"""
    dices = {}
    for i in range(1, 7):
        dices[i] = pygame.image.load(PATH + ("/resource/dice/%s.png" % str(i)))
    return dices


def load_card(deck: Deck):
    """Load card images"""
    deck_images = {}
    for card in deck.cards:
        card_image = pygame.image.load(PATH + '/resource/cards/%s.jpg' % str(card))
        card_image = pygame.transform.scale(card_image, (70, 110))
        deck_images[str(card)] = card_image
    return deck_images


def get_players():
    """"Load all players from file"""
    try:
        with open(PATH + '/resource/players.json', 'r') as players_file:
            players_dict = json.load(players_file)
            players_file.close()
            return players_dict
    except Exception as exc:
        print("error" + str(exc))


# Get Dice Images for later use
dice_imag = get_dice_images()


# Functions for the games logic
def show_dice_winner(players):
    """Dice Game winner"""
    counter = 1
    lane_c = 15
    screen_background(bg_surf, bg_logo)
    score_label = my_font.render("P SCORE    NAME", False, BLACK)
    screen.blit(score_label, (0, 0))
    rank_players = OrderedDict(sorted(players.items(), key=lambda kv: kv[1]["score"]["dice_score"], reverse=True))
    for player, value in rank_players.items():
        score_val = value["score"]["dice_score"]
        if score_val == 0:
            continue

        full_name = value["name"]["first_name"] + " " + value["name"]["last_name"]
        player_score = my_font.render("%s.   %s       %s" % (str(counter), str(score_val), full_name), False, BLACK)
        screen.blit(player_score, (0, lane_c))
        lane_c += 20
        counter += 1


def show_player_scores(players, game_of_dice=False):
    """Players Scores depending if dice or Card game"""
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
    """Random roll depending the player type"""
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
    """Dice Game"""
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
    if pl1["player_num"] in pl2["games"]["dice_players_played"] or \
            pl2["player_num"] in pl1["games"]["dice_players_played"]:
        return cpl_list
    pl1["games"]["dice_players_played"].append(pl2["player_num"])
    pl2["games"]["dice_players_played"].append(pl1["player_num"])

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


def show_all_cards(players, card_players, card_images):
    """Show all cards function. implemented for debugging"""
    screen3 = pygame.display.set_mode((DISPLAY_WIDTH - 500, DISPLAY_HEIGHT + 130))
    screen3.fill(LGREEN)
    screen3.blit(bg_logo, (DISPLAY_WIDTH - 930, -60))
    player_pic2 = pygame.transform.scale(player_pic, (50, 50))
    height_c = 0
    for cpl in card_players:
        width_c = 0
        pl_name = my_font.render(players[str(cpl)]["name"]["first_name"] + " " +
                                 players[str(cpl)]["name"]["last_name"], False, (40, 40, 40))
        screen3.blit(player_pic2, (10, 20 + height_c))
        screen3.blit(pl_name, (80, 50 + height_c))
        for card in players[str(cpl)]["score"]["cards"]:
            card_image = pygame.transform.scale(card_images[card], (50, 90))
            screen3.blit(card_image, (210 + width_c, 20 + height_c))
            width_c += 55
        height_c += 95


def show_card_winner(players, card_players, card_images):
    """Show Winner"""
    screen2 = pygame.display.set_mode((DISPLAY_WIDTH - 500, DISPLAY_HEIGHT - 300))
    screen2.fill(LGREEN)
    screen2.blit(bg_logo, (DISPLAY_WIDTH - 930, -60))
    player_pic2 = pygame.transform.scale(player_pic, (50, 50))
    height_c = 0
    pl_aces = []
    pl_counter = 0
    for cpl in card_players:
        if players[str(cpl)]["score"]["aces"] > 0:
            pl_counter += 1
            pl_aces.append([players[str(cpl)]["name"]["first_name"], players[str(cpl)]["score"]["aces"]])
            width_c = 0
            pl_name = my_font.render(players[str(cpl)]["name"]["first_name"] + " " +
                                     players[str(cpl)]["name"]["last_name"], False, (40, 40, 40))
            screen2.blit(player_pic2, (10, 20 + height_c))
            screen2.blit(pl_name, (80, 50 + height_c))
            for card in players[str(cpl)]["score"]["cards"]:
                card_image = pygame.transform.scale(card_images[card], (50, 90))
                screen2.blit(card_image, (210 + width_c, 20 + height_c))
                width_c += 55
            height_c += 95
    pl_aces.sort(key=lambda x: x[1], reverse=True)
    print(pl_aces)
    win_draw = "Winner is : %s" % pl_aces[0][0] if pl_counter % 2 != 0 and len(pl_aces) < 4 else "No winner. Its a Draw"

    win_name = my_font.render(win_draw, False, (40, 40, 40))
    screen2.blit(win_name, (700, 250))


def card_game(players, card_players):
    """Card Game"""
    screen_background(bg_surf, bg_logo)
    deck = Deck()
    card_images = load_card(deck)
    if not card_players:
        no_pl_label = my_font.render("There are no Card Players... Restart the game", False, (40, 40, 40))
        screen.blit(no_pl_label, (700, 300))
    else:
        for player in players:
            players[player]["games"]["card_games"] += 1
        deck.deck_shuffle()
        while deck.cards:
            for cpl in card_players:
                width_c = 600
                if deck.cards:
                    screen_background(bg_surf, bg_logo)
                    show_player_scores(players, False)
                    pl_name = my_font.render(players[str(cpl)]["name"]["first_name"], False, (40, 40, 40))
                    screen.blit(player_pic, (450, 350))
                    screen.blit(pl_name, (450, 320))
                    card_picked = str(deck.draw())
                    players[str(cpl)]["score"]["cards"].append(card_picked)
                    if "ACE" in card_picked:
                        players[str(cpl)]["score"]["aces"] += 1
                    for card in players[str(cpl)]["score"]["cards"]:
                        screen.blit(card_images[card], (width_c, 350))
                        width_c += 70
                    pygame.display.flip()
                    # time.sleep(0.1)
    show_card_winner(players, card_players, card_images)


def main():
    """ Main program function. """
    # Get the players dict
    card_player_list = []
    space_hit_first = True
    players_list = get_players()
    pygame.display.flip()
    screen_background(bg_surf, bg_logo)
    label = my_font.render("Press SPACE to START the DICE game!", False, (40, 40, 40))
    screen.blit(label, (770, 300))

    # Game Loop
    game_running = True
    while game_running:
        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_running = False
                if event.key == pygame.K_SPACE and space_hit_first:
                    space_hit_first = False
                    screen_background(bg_surf, bg_logo)
                    show_player_scores(players_list)
                    card_player_list = meeting(players_list)
                    show_dice_winner(players_list)
                    label = my_font.render("Click on Joker to continue to CARDS game!", False, (40, 40, 40))
                    screen.blit(label, (750, 300))
                    screen.blit(joker, (860, 500))
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(mouse)
                if 855 < mouse[0] < 965 and 480 < mouse[1] < 600:
                    card_game(players_list, card_player_list)

        pygame.display.update()
        clock.tick(120)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
