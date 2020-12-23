import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import datetime as dt
from pathlib import Path
import os

pd.set_option('display.max_columns', None)


class PokedexData:
    def __init__(self, overwrite_results_path=False):
        self.url = r'https://pokemondb.net/pokedex/all'
        self.overwrite_results_path = overwrite_results_path

    def get_pokedex_data(self):
        # TODO add a check for successful response
        webpage = requests.get(self.url)
        soup = BeautifulSoup(webpage.content, 'html.parser')
        pokedex_uncleaned = soup.findAll('tr')

        pokedex_data_ls = []
        header_row = pokedex_uncleaned[0].text.strip()
        header_row = header_row.replace('Sp. ', 'Special_').split()
        for row in pokedex_uncleaned[1:]:
            types = [re.sub(r'^.*?>', '', str(x))[:-4] for x in row.findAll('a', class_='type-icon')]
            name = row.a.text.strip()
            row = row.text.strip().replace('\n', ' ').split()
            row[1] = name
            row.insert(2, '_'.join(types))

            # Expecting a numeric value for Total
            while len(row) > len(header_row):
                try:
                    row[3] = float(row[3])
                except ValueError:
                    row.pop(3)
            pokedex_data_ls.append(row)

        pokedex_df = pd.DataFrame(columns=header_row, data=pokedex_data_ls)
        # only keep first occurance
        pokedex_df.drop_duplicates(subset='#', keep='first', inplace=True)
        pokedex_df.index = range(len(pokedex_df))
        return pokedex_df

    def __call__(self):
        pokedex_df = self.get_pokedex_data()
        print(pokedex_df.head())

        if self.overwrite_results_path:
            pokedex_df['Update_Time'] = dt.datetime.now()
            pokedex_df.to_csv(self.overwrite_results_path)


if __name__ == '__main__':
    mfs_path = os.path.join(str(Path(__file__).parents[0]), 'mfs')
    overwrite_results_path = os.path.join(mfs_path, 'pokedex_data.csv')

    x = PokedexData(overwrite_results_path=overwrite_results_path)
    x()
