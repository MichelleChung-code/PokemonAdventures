import battle_simulation.constants as const
from battle_simulation.Pokemon import Pokemon
from battle_simulation.battle_common import unittest_failure_msg
import unittest
import os
from pathlib import Path
import pandas as pd
import json
import copy


class PokemonUnitTests(unittest.TestCase):
    def setUp(self):
        mfs_path = os.path.join(str(Path(__file__).parents[0]), 'pokemon_unittests_data')
        self.pokemon_df = pd.read_csv(os.path.join(mfs_path, 'pokedex_data.csv'), index_col=2)
        self.pokemon_df.drop('Unnamed: 0', axis=1, inplace=True)
        self.status_effect_df = pd.read_csv(os.path.join(mfs_path, 'status_effects.csv'), index_col=0)
        moveset_json = os.path.join(mfs_path, 'moveset.json')
        with open(moveset_json) as json_file:
            moveset_data = json.load(json_file)

        self.dummy_mon = Pokemon('Mew', self.pokemon_df, moveset_data['Mew'], self.status_effect_df)

    def test_only_4_moves(self):
        """ Test that exception is raised when number of moves in provided moveset is not equal to 4 """
        dummy_move = {'5': {'dummy_move': {'power': 100, 'accuracy': 100, 'status': False}}}
        invalid_moveset = copy.deepcopy(self.dummy_mon.moveset)
        invalid_moveset.update(dummy_move)  # invalid since contains 5 moves
        name = 'Mew'
        with self.assertRaises(Exception) as context:
            Pokemon(name, self.pokemon_df, invalid_moveset, self.status_effect_df)

        self.assertTrue('{} moveset does not contain 4 moves.'.format(name) in str(context.exception),
                        unittest_failure_msg('exception not thrown when moveset does not contain 4 moves'))

    # todo need to add unittests for all the status effects
    def test_status_effect_skip_turn(self):
        """ Test that frozen pokemon move did not effect other one, i.e. turn was skipped """
        dummy_mon_1 = copy.deepcopy(self.dummy_mon)

        dummy_move = {'1': {'dummy_move': {'power': 100, 'accuracy': 100, 'status': False}}}
        dummy_mon_2 = copy.deepcopy(self.dummy_mon)
        dummy_mon_2.moveset.update(dummy_move)
        dummy_mon_2.status_effect = 'frozen'

        dummy_mon_2.use_move(dummy_mon_1, 1)

        self.assertEqual(dummy_mon_1.max_hp, dummy_mon_1.hp,
                         unittest_failure_msg('pokemon with frozen status still inflicting damage'))

    def test_status_effect_damage(self):
        """ Test that 'Damage_' status effect is working """
        dummy_mon_1 = copy.deepcopy(self.dummy_mon)
        dummy_mon_2 = copy.deepcopy(self.dummy_mon)

        dummy_mon_1.status_effect = 'poisoned'
        dummy_move = {'1': {'dummy_move': {'power': 100, 'accuracy': 100, 'status': False}}}
        dummy_mon_1.moveset.update(dummy_move)

        # pokemon should be damaged at the beginning of its turn
        dummy_mon_1.use_move(dummy_mon_2, 1)

        damage_perc = float(self.status_effect_df.loc[dummy_mon_1.status_effect, const.EFFECT_1].split('_')[1])

        damage = (damage_perc / 100) * dummy_mon_1.max_hp

        self.assertEqual(dummy_mon_1.hp, dummy_mon_1.max_hp - damage,
                         unittest_failure_msg('Damage_ status effect not yielding expected results'))

    def test_status_effect_damage_increasing(self):
        """ Test 'Damage_Incr' statuses i.e. badly poisoned """
        dummy_mon_1 = copy.deepcopy(self.dummy_mon)
        dummy_mon_2 = copy.deepcopy(self.dummy_mon)

        dummy_mon_1.status_effect = 'badly poisoned'
        dummy_move = {'1': {'dummy_move': {'power': 100, 'accuracy': 100, 'status': False}}}
        dummy_mon_1.moveset.update(dummy_move)
        damage_perc = float(self.status_effect_df.loc[dummy_mon_1.status_effect, const.EFFECT_1].split('_')[1])

        damage = 0
        for i in range(1, 4):
            dummy_mon_1.use_move(dummy_mon_2, 1)
            damage += (damage_perc / 100 * dummy_mon_1.max_hp) * i  # damage increases per turn
            self.assertEqual(dummy_mon_1.hp, dummy_mon_1.max_hp - damage, unittest_failure_msg(
                'Damage_Incr status effect not yielding expected results'))  # check damage caused at the end of each turn

    def test_status_effect_attack_stat(self):
        """ Test status impacting base attack stat i.e. burned """
        dummy_mon_1 = copy.deepcopy(self.dummy_mon)
        dummy_mon_2 = copy.deepcopy(self.dummy_mon)

        dummy_mon_1.status_effect = 'burned'
        dummy_mon_1_max_attack = dummy_mon_1.attack
        dummy_move = {'1': {'dummy_move': {'power': 100, 'accuracy': 100, 'status': False}}}
        dummy_mon_1.moveset.update(dummy_move)

        stat_decr_perc = float(self.status_effect_df.loc[dummy_mon_1.status_effect, const.EFFECT_2].split('_')[1])
        dummy_mon_1.use_move(dummy_mon_2, 1)

        self.assertEqual(dummy_mon_1.attack, dummy_mon_1_max_attack - (dummy_mon_1_max_attack * stat_decr_perc / 100),
                         unittest_failure_msg('attack stat impacting status effect not yielding expected results'))

        # Check that this decrease was only applied during the first turn that the status effect was effective
        dummy_mon_1.use_move(dummy_mon_2, 1)  # should not impact base attack stat
        self.assertEqual(dummy_mon_1.attack, dummy_mon_1_max_attack - (dummy_mon_1_max_attack * stat_decr_perc / 100),
                         unittest_failure_msg('attack stat impacting status effect being applied past the first turn'))
