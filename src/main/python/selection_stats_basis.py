import os
from pathlib import Path
import pandas as pd
import battle_simulation.constants as const

TOL = 1e-10


class StatsBasedTeam:
    def __init__(self, importance_df, pokemon_df):
        """
        Args:
            importance_df: <pd.DataFrame> with importance weights per stat
            pokemon_df: <pd.DataFrame> containing pokemon and available stat info
        """
        self.importance_df = importance_df
        self.pokemon_df = pokemon_df

        assert abs(sum(self.importance_df[const.VALUE]) - 1) <= TOL  # weights should sum to 1

    def select_team(self):
        """
        Function that scales and returns the top 6 choices based on importance df

        Returns: <list> of chosen 6 pokemon
        """
        # apply the importance weights i.e. how much do you care about the particular stat

        for stat in const.STATS_LS:
            self.pokemon_df[stat] *= self.importance_df.loc[stat][0]

        overall_score_series = self.pokemon_df[const.STATS_LS].sum(axis=1)

        # get top 6 scores
        return overall_score_series.nlargest(6).index.to_list()


if __name__ == '__main__':
    mfs_path = os.path.join(str(Path(__file__).parents[3]), 'mfs')
    pokemon_df = pd.read_csv(os.path.join(mfs_path, 'pokedex_data.csv'), index_col=2)
    pokemon_df.drop('Unnamed: 0', axis=1, inplace=True)

    stats_importance_df = pd.read_csv(os.path.join(mfs_path, 'stat_importance.csv'), index_col=0)

    x = StatsBasedTeam(stats_importance_df, pokemon_df)
    print(sorted(x.select_team(), key=str.lower))
