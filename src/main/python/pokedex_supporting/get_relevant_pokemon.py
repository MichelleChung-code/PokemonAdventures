import copy
import difflib
import os
from pathlib import Path

import pandas as pd

STAT_COLS = ['HP', 'Attack', 'Defense', 'Special_Atk', 'Special_Def', 'Speed']

# This dictionary needs to be ordered in increasing relative strength
PERCENTILES_MAP = {'weak': 0.1,
                   'bad': 0.25,
                   'average': 0.5,
                   'good': 0.75,
                   'strong': 0.95}

# In case it was not sorted
PERCENTILES_MAP = dict(sorted(PERCENTILES_MAP.items(), key=lambda item: item[1]))


def compute_percentiles(df_pokedex):
    dict_map_strength = copy.deepcopy(PERCENTILES_MAP)
    df_pokedex = df_pokedex[STAT_COLS]

    for k, v in dict_map_strength.items():
        dict_map_strength[k] = df_pokedex.quantile(v)

    return dict_map_strength


def get_relevant(df_pokedex, dict_relative_attr_strength, attribute_desc):
    ls_diff_attributes = attribute_desc.split(',')
    ls_diff_attributes = [x.strip() for x in ls_diff_attributes]
    dict_actual_attr = {''.join(x.split(' ')[1:]): x.split(' ')[0] for x in ls_diff_attributes}
    dict_processed_attr = dict()
    for k, v in dict_actual_attr.items():
        k_processed = difflib.get_close_matches(k.lower(), list(map(str.lower, STAT_COLS)), n=1)
        v_processed = difflib.get_close_matches(v.lower(), list(map(str.lower, dict_relative_attr_strength.keys())),
                                                n=1)

        assert k_processed and v_processed, f'Invalid User Input {k}, {v}'
        assert len(k_processed) == len(v_processed) == 1

        dict_processed_attr[k_processed[0]] = v_processed[0]

    # let's work in all lowercases
    df_pokedex.columns = df_pokedex.columns.str.lower()

    print('sd')


if __name__ == '__main__':
    mfs_path = os.path.join(str(Path(__file__).parents[0]), '../../../../mfs')
    pokedex_data = os.path.join(mfs_path, 'pokedex_data.csv')

    df_pokedex = pd.read_csv(pokedex_data, index_col=0)
    relative_strength_attributes_dict = compute_percentiles(df_pokedex)

    str_desc = 'strong hp, weaker speed, good special attack'
    print(get_relevant(df_pokedex=df_pokedex, dict_relative_attr_strength=relative_strength_attributes_dict,
                       attribute_desc=str_desc))

    # while True:
    #     str_desc = input('Enter some key attributes: ')
    #     if str_desc == 'exit':
    #         break
    #     get_relevant(df_pokedex)
    #
    # print('Be happy! :)')
