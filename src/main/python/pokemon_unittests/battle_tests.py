from battle_simulation.Pokemon import Pokemon
from battle_simulation.Battle import Battle
import os
import pandas as pd
from pathlib import Path
import copy
import json
from battle_simulation.battle_common import unittest_failure_msg
import unittest


class BattleUnitTests(unittest.TestCase):
    def setUp(self):
        mfs_path = os.path.join(str(Path(__file__).parents[0]), 'pokemon_unittests_data')
        pokemon_df = pd.read_csv(os.path.join(mfs_path, 'pokedex_data.csv'), index_col=2)
        pokemon_df.drop('Unnamed: 0', axis=1, inplace=True)
        status_effect_df = pd.read_csv(os.path.join(mfs_path, 'status_effects.csv'), index_col=0)
        moveset_json = os.path.join(mfs_path, 'moveset.json')
        with open(moveset_json) as json_file:
            moveset_data = json.load(json_file)

        self.dummy_mon_1 = Pokemon('Mew', pokemon_df, moveset_data['Mew'], status_effect_df)
        self.dummy_mon_2 = Pokemon('Mewtwo', pokemon_df, moveset_data['Mewtwo'], status_effect_df)

    def test_max_hp_remains_same(self):
        """ Run battle between the two pokemon and check that max hp does not change """
        dummy_mon_1 = copy.deepcopy(self.dummy_mon_1)
        dummy_mon_2 = copy.deepcopy(self.dummy_mon_2)
        dummy_1_max_hp = dummy_mon_1.max_hp
        dummy_2_max_hp = dummy_mon_2.max_hp

        Battle(dummy_mon_1, dummy_mon_2).execute_battle()

        self.assertEqual(dummy_mon_1.max_hp, dummy_1_max_hp, unittest_failure_msg('battle has changed pokemon max HP'))
        self.assertEqual(dummy_mon_2.max_hp, dummy_2_max_hp, unittest_failure_msg('battle has changed pokemon max HP'))
