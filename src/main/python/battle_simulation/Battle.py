from battle_simulation.Pokemon import Pokemon
import os
import pandas as pd
from pathlib import Path
from battle_simulation import constants as const
import copy


class Battle:

    def __init__(self, Pokemon1, Pokemon2):
        """
        Args:
            Pokemon1: <Pokemon> first Pokemon
            Pokemon2: <Pokemon> second Pokemon
        """
        self.Pokemon1 = Pokemon1
        self.Pokemon2 = Pokemon2

    def execute_battle(self):
        """
        Runs the turn based auto-battle, randomized moves
        """
        print('Battle started between: {0} and {1}'.format(self.Pokemon1.name, self.Pokemon2.name))
        while self.Pokemon1.hp > 0 and self.Pokemon2.hp > 0:
            if self.Pokemon1.speed >= self.Pokemon2.speed:
                self.Pokemon1.use_move(self.Pokemon2)
                self.Pokemon2.use_move(self.Pokemon1)
            else:
                self.Pokemon2.use_move(self.Pokemon1)
                self.Pokemon1.use_move(self.Pokemon2)
        winner = self.Pokemon1.name if self.Pokemon1.hp > 0 else self.Pokemon2.name
        return winner


def experiment_winner(Battle, num_battles, name_expected_winner):
    """
    Args:
        Battle: <Battle> Battle instance to evaluate against
        num_battles: <int> number of battles to run to calculate probability
        name_expected_winner: <str> name of the Pokemon to calculate its probability of winnning

    Returns: <float> Probability for the expected winner to win the battle.
    """
    if name_expected_winner not in [Battle.Pokemon1.name, Battle.Pokemon2.name]:
        raise Exception('Given expected winner name not involved in given battle.')

    successful_wins = 0
    for i in range(num_battles):
        new_battle = copy.deepcopy(Battle)
        if new_battle.execute_battle() == name_expected_winner:
            successful_wins += 1

    return 'Probability of {0} winning: {1}'.format(name_expected_winner, successful_wins / num_battles)


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

    # todo better control of the console outputs
    print(experiment_winner(battle, 1000, 'Mewtwo'))
