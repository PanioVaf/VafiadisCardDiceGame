import unittest
import random

from src.deck import Deck


class TestStringMethods(unittest.TestCase):

    def test_deck_size(self):
        deck = Deck()
        self.assertEqual(len(deck.cards), 52)
        self.assertTrue(deck.has_cards())

        for i in range(52):
            deck.take_card()

        self.assertFalse(deck.has_cards())

    def test_deck_shuffle(self):
        deck = Deck()
        random.seed(2020)
        before = deck.cards.copy()
        deck.shuffle()
        after = deck.cards.copy()
        self.assertCountEqual(before, after)
        self.assertNotEqual(before, after)


if __name__ == '__main__':
    unittest.main()
