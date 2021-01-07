from pathlib import Path
import plotly.express as px
import os
import pandas as pd
import battle_simulation.constants as const


class PokemonAttributePlot:
    def __init__(self, pokemon_df, pokemon_name):
        """
        Args:
            pokemon_df: <pd.DataFrame> containing pokemon stat information
            pokemon_name: <str> name of pokemon to plot
        """
        self.pokemon_df = pokemon_df.loc[pokemon_name]
        self.pokemon_name = pokemon_name
        self.results_path = os.path.join(str(Path(__file__).parents[0]), 'results')

    def preprocess(self):
        """ Some initial data cleaning/ reformatting """
        # clean data to be ready to plot
        cols_to_plot = [const.HP, const.ATTACK, const.DEFENSE, const.SP_ATTACK, const.SP_DEFENSE, const.SPEED]
        self.pokemon_df = self.pokemon_df.loc[cols_to_plot].to_frame().reset_index()
        self.pokemon_df.rename(columns={'index': const.ATTRIBUTE, self.pokemon_name: const.VALUE}, inplace=True)

    def plot_attributes(self):
        """ Plots the attributes in a polar plot using plotly """
        # https://plotly.com/python/templates/

        fig = px.line_polar(self.pokemon_df, r=const.VALUE, range_r=(0, max(self.pokemon_df[const.VALUE].max(), 100)),
                            title='{} Attributes'.format(self.pokemon_name), theta=const.ATTRIBUTE,
                            template='seaborn', line_close=True)
        fig.to_image(format="png", engine="kaleido")
        fig.write_image(os.path.join(self.results_path, '{}.png'.format(self.pokemon_name)))

    def __call__(self):
        """ Calls the data cleaning and plotting functions  """
        self.preprocess()
        self.plot_attributes()


# https://medium.com/@marcosanchezayala/plotting-pokemon-attributes-plotly-polar-plots-and-animations-319934b60f0e
if __name__ == '__main__':
    mfs_path = os.path.join(str(Path(__file__).parents[4]), 'mfs')
    pokemon_df = pd.read_csv(os.path.join(mfs_path, 'pokedex_data.csv'), index_col=2)
    pokemon_df.drop('Unnamed: 0', axis=1, inplace=True)

    name_to_plot = 'Charmander'

    x = PokemonAttributePlot(pokemon_df, name_to_plot)
    x()
