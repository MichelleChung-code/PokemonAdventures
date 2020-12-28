from battle_simulation.Pokemon import Pokemon
import os
import pandas as pd
from pathlib import Path
from battle_simulation import constants as const


class Battle:

    def __init__(self, Pokemon1, Pokemon2):
        """

        Args:
            Pokemon1: <Pokemon>
            Pokemon2: <Pokemon>
        """
        self.Pokemon1 = Pokemon1
        self.Pokemon2 = Pokemon2

    def execute_battle(self):
        print('Battle started between: {0} and {1}'.format(self.Pokemon1.name, self.Pokemon2.name))
        while self.Pokemon1.hp > 0 and self.Pokemon2.hp > 0:
            if self.Pokemon1.speed >= self.Pokemon2.speed:
                self.Pokemon1.use_move(self.Pokemon2)
                self.Pokemon2.use_move(self.Pokemon1)
            else:
                self.Pokemon2.use_move(self.Pokemon1)
                self.Pokemon1.use_move(self.Pokemon2)


def experiment_winner():
    pass


if __name__ == '__main__':
    mfs_path = os.path.join(str(Path(__file__).parents[4]), 'mfs', 'pokedex_data.csv')
    pokemon_df = pd.read_csv(mfs_path, index_col=2)
    pokemon_df.drop('Unnamed: 0', axis=1, inplace=True)
    # todo maybe put movesets in a JSON
    Mewtwo_moveset = {1: {'Confusion': {const.POW: 50, const.ACC: 100}}, 2: {'Psywave': {const.POW: 1, const.ACC: 80}},
                      3: {'Psybeam': {const.POW: 65, const.ACC: 100}}, 4: {'Psychic': {const.POW: 90, const.ACC: 100}}}
    Mewtwo = Pokemon('Mewtwo', pokemon_df, Mewtwo_moveset)

    Mew_moveset = {1: {'Confusion': {const.POW: 50, const.ACC: 100}}, 2: {'Pound': {const.POW: 40, const.ACC: 100}},
                   3: {'Mega Punch': {const.POW: 80, const.ACC: 85}}, 4: {'Psychic': {const.POW: 90, const.ACC: 100}}}

    Mew = Pokemon('Mew', pokemon_df, Mew_moveset)

    battle = Battle(Mewtwo, Mew)
    battle.execute_battle()
