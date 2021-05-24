from selection_stats_basis import StatsBasedTeam
import unittest
import os
from pathlib import Path
import pandas as pd


class SelectionUnitTests(unittest.TestCase):
    def setUp(self):
        mfs_path = os.path.join(str(Path(__file__).parents[0]), 'pokemon_unittests_data')
        self.pokemon_df = pd.read_csv(os.path.join(mfs_path, 'pokedex_data.csv'), index_col=2)
        self.pokemon_df.drop('Unnamed: 0', axis=1, inplace=True)
        self.stats_importance_df = pd.read_csv(os.path.join(mfs_path, 'stat_importance.csv'), index_col=0)

    def test_selection(self):
        x = StatsBasedTeam(self.stats_importance_df, self.pokemon_df)
        res_ls = sorted(x.select_team(), key=str.lower)

        self.assertEqual(res_ls, ['Groudon', 'Regigigas', 'Slaking', 'Zacian', 'Zamazenta', 'Zekrom'])
        self.assertTrue(len(res_ls) == 6)  # should only contain 6 items
