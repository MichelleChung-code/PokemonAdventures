import copy
import os
from pathlib import Path

import pandas as pd

STAT_COLS = ['HP', 'Attack', 'Defense', 'Special_Atk', 'Special_Def', 'Speed']
PERCENTILES_MAP = {'weak': 0.1,
                   'bad': 0.25,
                   'average': 0.5,
                   'good': 0.75,
                   'strong': 0.95}


def compute_percentiles(df_pokedex):
    dict_map_strength = copy.deepcopy(PERCENTILES_MAP)
    df_pokedex = df_pokedex[STAT_COLS]

    for k, v in dict_map_strength.items():
        dict_map_strength[k] = df_pokedex.quantile(v)

    return dict_map_strength


def get_relevant(df_pokedex, attribute_desc):
    print('sd')


if __name__ == '__main__':
    mfs_path = os.path.join(str(Path(__file__).parents[0]), '../../../../mfs')
    pokedex_data = os.path.join(mfs_path, 'pokedex_data.csv')

    df_pokedex = pd.read_csv(pokedex_data, index_col=0)
    relative_strength_attributes_dict = compute_percentiles(df_pokedex)

    str_desc = 'strong hp, weaker speed, good special attack'
    print(get_relevant(str_desc))

    # while True:
    #     str_desc = input('Enter some key attributes: ')
    #     if str_desc == 'exit':
    #         break
    #     get_relevant(df_pokedex)
    #
    # print('Be happy! :)')
