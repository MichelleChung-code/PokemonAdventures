import copy
import difflib
import os
import unittest
from pathlib import Path

import pandas as pd

STAT_COLS = ['HP', 'Attack', 'Defense', 'Special_Atk', 'Special_Def', 'Speed']
STAT_COLS_LOWER = list(map(str.lower, STAT_COLS))

# This dictionary needs to be ordered in increasing relative strength
PERCENTILES_MAP = {'weak': 0.1,
                   'bad': 0.25,
                   'average': 0.5,
                   'good': 0.75,
                   'strong': 0.95}

# In case it was not sorted
PERCENTILES_MAP = dict(sorted(PERCENTILES_MAP.items(), key=lambda item: item[1]))


def compute_percentiles(df_pokedex):
    """
    Get percentile values per stat type to map to a relative strength

    Args:
        df_pokedex: <pd.DataFrame> containing the pokedex data

    Returns:
        <dict> of relative strength keys and dataframe values for the lower bound value per stat type
    """
    dict_map_strength = copy.deepcopy(PERCENTILES_MAP)
    df_pokedex = df_pokedex[STAT_COLS_LOWER]

    for k, v in dict_map_strength.items():
        dict_map_strength[k] = df_pokedex.quantile(v)

    return dict_map_strength


def get_relevant(df_pokedex, dict_relative_attr_strength, attribute_desc):
    """
    Filter the pokedex with the given input attributes

    Args:
        df_pokedex: <pd.DataFrame> containing the pokedex data
        dict_relative_attr_strength: <dict> of relative strength keys and dataframe values for the lower bound value per stat type
        attribute_desc: <str> input attributes separated by commas

    Returns:
        <list> relevent pokemon meeting the input condition
    """
    ls_diff_attributes = attribute_desc.split(',')
    ls_diff_attributes = [x.strip() for x in ls_diff_attributes]
    dict_actual_attr = {''.join(x.split(' ')[1:]): x.split(' ')[0] for x in ls_diff_attributes}
    dict_processed_attr = dict()

    for k, v in dict_actual_attr.items():
        k_processed = difflib.get_close_matches(k.lower(), list(map(str.lower, STAT_COLS)), n=1)

        # the processed dictionary should have no duplicates
        if k_processed[0] in dict_processed_attr.keys():
            raise Exception('Cannot input the same stat attribute more than once')

        v_processed = difflib.get_close_matches(v.lower(), list(map(str.lower, dict_relative_attr_strength.keys())),
                                                n=1)

        assert k_processed and v_processed, f'Invalid User Input {k}, {v}'
        assert len(k_processed) == len(v_processed) == 1

        # and map to the ranges
        starting = dict_relative_attr_strength[v_processed[0]][k_processed[0]]
        starting_index = list(dict_relative_attr_strength.keys()).index(v_processed[0])

        if starting_index == len(dict_relative_attr_strength.keys()) - 1:
            ending = float('inf')
        else:
            ending = dict_relative_attr_strength[list(dict_relative_attr_strength.keys())[starting_index + 1]][
                k_processed[0]]

        dict_processed_attr[k_processed[0]] = [starting, ending]

    # we need to filter for the mons that match these attributes
    # create a nice condition string to do this
    str_bool_ls = []
    for k, v in dict_processed_attr.items():
        str_bool_ls.append(f'{v[0]} <= {k} <= {v[1]}')

    str_bool = ' and '.join(str_bool_ls)
    df_filtered = df_pokedex.loc[df_pokedex.eval(str_bool)]

    return sorted(list(set(df_filtered.name.values)))


class PokedexSubset(unittest.TestCase):

    def test_expected_result(self):
        """ Simple unittest that we return expected results """
        mfs_path = os.path.join(str(Path(__file__).parents[0]), '../../../../mfs')
        pokedex_data = os.path.join(mfs_path, 'pokedex_data.csv')
        df_pokedex = pd.read_csv(pokedex_data, index_col=0)

        str_desc = 'average hp'
        lb = df_pokedex['HP'].quantile(0.5)
        ub = df_pokedex['HP'].quantile(0.75)

        expected = df_pokedex.loc[df_pokedex['HP'].between(lb, ub, inclusive=True)]
        expected = sorted(list(set(expected['Name'].values)))

        df_pokedex.columns = df_pokedex.columns.str.lower()
        relative_strength_attributes_dict = compute_percentiles(df_pokedex)

        res = get_relevant(df_pokedex, relative_strength_attributes_dict, str_desc)

        self.assertEqual(expected, res)


if __name__ == '__main__':
    mfs_path = os.path.join(str(Path(__file__).parents[0]), '../../../../mfs')
    pokedex_data = os.path.join(mfs_path, 'pokedex_data.csv')

    df_pokedex = pd.read_csv(pokedex_data, index_col=0)
    # let's work in all lowercases
    df_pokedex.columns = df_pokedex.columns.str.lower()
    relative_strength_attributes_dict = compute_percentiles(df_pokedex)

    str_desc = 'strong hp'
    get_relevant(df_pokedex, relative_strength_attributes_dict, str_desc)

    while True:
        str_desc = input('Enter some key attributes: ')
        if str_desc == 'exit':
            break
        print(get_relevant(df_pokedex, relative_strength_attributes_dict, str_desc)['name'].values)

    print('YAY! :)')
