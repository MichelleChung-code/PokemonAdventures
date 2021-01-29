from battle_simulation.Pokemon import Pokemon
import os
import pandas as pd
from pathlib import Path
import logging
import copy
import json
from battle_simulation.battle_common import battle_log_msg


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
        battle_log_msg('Battle started between: {0} and {1}'.format(self.Pokemon1.name, self.Pokemon2.name))
        while self.Pokemon1.hp > 0 and self.Pokemon2.hp > 0:
            if self.Pokemon1.speed >= self.Pokemon2.speed:
                self.Pokemon1.use_move(self.Pokemon2)
                if self.Pokemon2.hp > 0:  # if Pokemon2 has already fainted
                    self.Pokemon2.use_move(self.Pokemon1)
            else:
                self.Pokemon2.use_move(self.Pokemon1)
                if self.Pokemon1.hp > 0:  # todo think of a better way to do this check
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
    print('Pokemon Battling: {0} and {1}'.format(Battle.Pokemon1.name, Battle.Pokemon2.name))

    successful_wins = 0
    for i in range(num_battles):
        battle_txt = ' Battle {} '.format(i + 1)
        num_equal_signs = (50 - len(battle_txt)) // 2
        logging.info('=' * num_equal_signs + battle_txt + '=' * num_equal_signs)
        new_battle = copy.deepcopy(Battle)
        battle_winner = new_battle.execute_battle()
        if battle_winner == name_expected_winner:
            successful_wins += 1
        print('Battle #{0} Winner: {1}'.format(i + 1, battle_winner))

    return 'Probability of {0} winning: {1}'.format(name_expected_winner, successful_wins / num_battles)

if __name__ == '__main__':
    # set up logging
    battle_log = os.path.join(str(Path(__file__).parents[0]), 'results', 'battle_log.txt')
    logging.basicConfig(filename=battle_log, filemode='w',
                        format='[%(name)s %(levelname)s] %(asctime)s.%(msecs)d - %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO)

    mfs_path = os.path.join(str(Path(__file__).parents[4]), 'mfs')
    print(mfs_path)
    pokemon_df = pd.read_csv(os.path.join(mfs_path, 'pokedex_data.csv'), index_col=2)
    pokemon_df.drop('Unnamed: 0', axis=1, inplace=True)

    status_effect_df = pd.read_csv(os.path.join(mfs_path, 'status_effects.csv'), index_col=0)

    moveset_json = os.path.join(mfs_path, 'moveset.json')
    with open(moveset_json) as json_file:
        moveset_data = json.load(json_file)

    Mewtwo_moveset = moveset_data['Mewtwo']
    Mewtwo = Pokemon('Mewtwo', pokemon_df, Mewtwo_moveset, status_effect_df)

    Mew_moveset = moveset_data['Mew']

    Mew = Pokemon('Mew', pokemon_df, Mew_moveset, status_effect_df)

    battle = Battle(Mewtwo, Mew)

    print(experiment_winner(battle, 1000, 'Mewtwo'))
