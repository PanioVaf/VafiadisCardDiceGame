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

import os
from pathlib import Path

from src.load_players import load_players
from src.simulator import Simulator


def main():
    """ Main program function. """
    resources_path = Path(os.path.dirname(os.path.abspath(__file__))).parent / 'resource'
    all_players = load_players(resources_path / 'players.json')
    simulator = Simulator(resources_path)
    simulator.run(all_players)


if __name__ == "__main__":
    main()
