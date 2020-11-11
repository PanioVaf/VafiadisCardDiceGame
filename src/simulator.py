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

import itertools
import os
import sys
import time
from enum import IntEnum

from src.card_match import CardMatch
from src.deck import Deck, Ranks
from src.dice_match import DiceMatch

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame  # declared after, due to pygame convention


class WindowGameMode(IntEnum):
    """Window screens enum"""
    STARTUP_SCREEN, DICE_GAME_SCREEN, JOKER_SCREEN, CARD_GAME_SCREEN, WINNER_GAME_SCREEN = range(1, 6)


class Simulator:
    def __init__(self, resources_path):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Welcome to John's Card Dice Game, developed by Panagiotis Vafiadis")
        self.mode = WindowGameMode.STARTUP_SCREEN
        self.resources_path = resources_path
        self.FONT_SIZE = 15
        self.DICE_ROLLS = 10
        self.BLACK = (0, 0, 0)
        self.GREEN = (40, 120, 80)
        self.RED = (130, 10, 0)
        self.LGREEN = (130, 200, 150)
        self.screen = pygame.display.set_mode((1200, 600))
        self.my_font = pygame.font.SysFont('Times New Roman', self.FONT_SIZE, True)
        self.bg_surf = self.load_image('table.jpg', (900, 600))
        self.bg_logo = self.load_image('ihu.png', (380, 240))
        self.joker = self.load_image('joker.jpg', (95, 80))
        self.player_pic = self.load_image('player.png', (80, 80))
        self.clock = pygame.time.Clock()
        self.dice_imag = self.load_dice_images()
        self.card_images = self.load_card(Deck())

    def load_image(self, image_file_name, scale):
        res = self.resources_path / image_file_name
        return pygame.transform.scale(pygame.image.load(str(res)), scale)

    def draw_screen_background(self, image, logo):
        self.screen.fill(self.GREEN)
        self.screen.blit(image, (300, 0))
        self.screen.blit(logo, (570, -50))

    def load_dice_images(self):
        """Load dice images"""
        dices = {}
        for dice in range(1, 7):
            dices[dice] = self.load_image("dice/%s.png" % str(dice), (80, 82))
        return dices

    def load_card(self, deck: Deck):
        """Load card images"""
        deck_images = {}
        for card in deck.cards:
            deck_images[str(card)] = self.load_image("cards/%s.jpg" % str(card), (70, 110))
        return deck_images

    def dice_game(self, dice_players):
        """Dice Game"""
        game_counter = 1
        for pl1, pl2 in itertools.combinations(dice_players, 2):
            match = DiceMatch(pl1, pl2)
            print()
            while match.playing():
                self.render_background()

                label = "{first_id}. {first_name}{gap}VS{gap}{second_id}. {second_name}".format(
                    first_id=pl1.player_id,
                    first_name=pl1.first_name,
                    gap=" " * 8,
                    second_id=pl2.player_id,
                    second_name=pl2.first_name)

                round_counter = match.get_current_round()
                self.render_text(label, (655, 200))
                self.render_text("Round %s" % str(round_counter), (730, 250))
                self.screen.blit(self.player_pic, (450, 380))
                self.screen.blit(self.player_pic, (970, 380))

                self.screen.blit(self.dice_imag[match.dice1], (580, 400))
                self.screen.blit(self.dice_imag[match.dice2], (850, 400))

                print("Game %s Round %s playing dice" % (game_counter, round_counter))
                print("%s vs %s | Dice1: %s Dice2: %s | Score1 : %s Score2: %s" % (
                    pl1.full_name, pl2.full_name, match.dice1, match.dice2, pl1.stats.dice_score, pl2.stats.dice_score))
                self.show_dice_winner(dice_players)
                pygame.display.flip()
                time.sleep(0.018)

    def show_player_scores(self, players):
        """Players Scores depending if dice or Card game"""

        lane_c = 0
        for player in players:
            names = " (%s) %s is a %s" % (player.player_id,
                                          player.first_name,
                                          player.player_type_desc)

            player_names = self.my_font.render(names, False, (0, 0, 0))

            player_score = self.my_font.render(" Cards:%sDice:%s  Ace:" % (" " * 8, " " * 10), False, (0, 0, 0))
            player_score_col = self.my_font.render(
                "%s%s%s%s%s%s" % (" " * 9, len(player.stats.cards),
                                  " " * 14, player.stats.dice_score,
                                  " " * 18, player.stats.aces), False, self.RED)

            print(names + " cards: " + (','.join(map(lambda c: str(c), player.stats.cards))))
            self.screen.blit(player_names, (2, lane_c))
            self.screen.blit(player_score, (32, lane_c + self.FONT_SIZE + 3))
            self.screen.blit(player_score_col, (52, lane_c + self.FONT_SIZE + 3))
            lane_c += (self.FONT_SIZE * 2.4)

    def show_dice_winner(self, players):
        """Dice Game winner"""

        counter = 1
        lane_c = 17
        self.render_text("P   SCORE    NAME", (2, 2), self.BLACK)

        rank_players = sorted(players, key=lambda x: x.stats.dice_score, reverse=True)

        for player in rank_players:
            score = player.stats.dice_score
            if not score:
                continue

            full_name = player.full_name
            gap = 7 if counter > 9 else 9
            self.render_text("%s.%s%s%s%s" % (str(counter), " " * gap, str(score), " " * 7, full_name), (2, lane_c), self.BLACK)
            lane_c += 20
            counter += 1

    def show_card_winner(self, card_match):
        """Show Card Winner"""

        self.screen.fill(self.LGREEN)
        self.render_image(self.bg_logo, (800, -60))

        player_pic2 = pygame.transform.scale(self.player_pic, (50, 50))
        height_c = 0
        for player in card_match.card_players:
            if player.stats.aces > 0:
                width_c = 0
                self.render_image(player_pic2, (10, 20 + height_c))
                self.render_text(player.full_name, (80, 50 + height_c))

                for card in player.stats.cards:
                    card_image = pygame.transform.scale(self.card_images[str(card)], (50, 90))
                    self.render_image(card_image, (210 + width_c, 20 + height_c))
                    width_c += 55
                height_c += 95

        winner = card_match.get_winner()
        win_draw = "Winner is: %s" % winner.full_name if winner else "No winner. It's a draw."
        self.render_text(win_draw, (900, 250))

    def render_text(self, message, pos, color=(40, 40, 40)):
        no_pl_label = self.my_font.render(message, False, color)
        self.screen.blit(no_pl_label, pos)

    def render_image(self, image, pos):
        self.screen.blit(image, pos)

    def render_background(self):
        self.draw_screen_background(self.bg_surf, self.bg_logo)

    def card_game(self, card_match):
        """Card Game"""
        self.render_background()
        deck = Deck()
        deck.shuffle()

        if not card_match.card_players:
            self.render_text("There are no Card Players... Restart the game", (620, 300))
        else:
            while card_match.deck.has_cards():
                for p in card_match.card_players:
                    width_c = 500
                    if card_match.playing(p):
                        self.render_background()
                        self.show_player_scores(card_match.card_players)
                        self.render_image(self.player_pic, (450, 350))
                        self.render_text(p.first_name, (450, 320))
                        pos = 1
                        for card in p.stats.cards:
                            self.render_image(self.card_images[str(card)], (width_c + 70 * pos, 350))
                            pos += 1

                        pygame.display.flip()
                        time.sleep(0.1)
                    else:
                        return

    def run(self, all_players):
        game_running = True
        dice_players = list(filter(lambda pl: pl.is_dice_player(), all_players))
        card_players = list(filter(lambda pl: pl.is_card_player(), all_players))
        card_match = CardMatch(card_players)

        print("All players:")
        for pl in all_players:
            print("  " + pl.full_name + " " + pl.player_type_desc)
        print("\nDice players:")
        for pl in dice_players:
            print("  " + pl.full_name + " " + pl.player_type_desc)
        print("\nCard players:")
        for pl in card_players:
            print("  " + pl.full_name + " " + pl.player_type_desc)
        print()

        while game_running:
            self.render_background()

            if self.mode == WindowGameMode.STARTUP_SCREEN:
                self.render_text("Press SPACE to START the DICE game or click!", (615, 300))
                pygame.display.flip()
            elif self.mode == WindowGameMode.DICE_GAME_SCREEN:
                self.dice_game(dice_players)
                self.mode = WindowGameMode.JOKER_SCREEN
            elif self.mode == WindowGameMode.JOKER_SCREEN:
                self.show_dice_winner(dice_players)
                self.render_text("Click on Joker to continue to CARDS game!", (615, 300))
                self.render_image(self.joker, (715, 400))
                pygame.display.flip()
            elif self.mode == WindowGameMode.CARD_GAME_SCREEN:
                self.card_game(card_match)
                self.mode = WindowGameMode.WINNER_GAME_SCREEN
            elif self.mode == WindowGameMode.WINNER_GAME_SCREEN:
                self.show_card_winner(card_match)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    game_running = False
                if self.mode == WindowGameMode.STARTUP_SCREEN:
                    if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or \
                            event.type == pygame.MOUSEBUTTONUP:
                        self.mode = WindowGameMode.DICE_GAME_SCREEN
                elif self.mode == WindowGameMode.JOKER_SCREEN:
                    mouse = pygame.mouse.get_pos()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if 730 < mouse[0] < 829 and 400 < mouse[1] < 480:
                            self.mode = WindowGameMode.CARD_GAME_SCREEN

            pygame.display.update()

        pygame.quit()
        sys.exit()
