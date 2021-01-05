# My python implementation of https://towardsdatascience.com/introduction-to-machine-learning-with-pokemon-ccb7c9d1351b
# CSV data taken from: https://drive.google.com/file/d/1nUwdfPHiqXmz8Zh89SxPSiIFwbm9IOvv/view

import pandas as pd
from imblearn.over_sampling import SMOTE
import machine_learning.constant as const
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression


class LegendaryPredictor:
    def __init__(self, pokemon_data_df):
        self.pokemon_data_df = pokemon_data_df

    @staticmethod
    def preprocessing(df, y_col):
        """
        Using the SMOTE approach, preprocess the data by creating test and train split oversampled data.  Oversampling
        applied to only the training data.

        Args:
            df: <pd.DataFrame> to apply preprocessing on
            y_col: <str> name of the column acting as dependent data

        Returns:
            <pd.DataFrames> X and y oversampled training data
        """
        # use SMOTE algorithm (Synthetic Minority Oversampling Technique)
        over_samp = SMOTE(random_state=0)
        X = df.loc[:, df.columns != y_col]
        X_cols = list(X.columns)
        y = df[y_col]

        # https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25,
                                                            random_state=0)  # just use default test_size=0.25

        X_os_data, y_os_data = over_samp.fit_sample(X_train, y_train)

        return pd.DataFrame(columns=X_cols, data=X_os_data), pd.DataFrame(columns=[y_col], data=y_os_data)

    def __call__(self):
        X_os_data, y_os_data = LegendaryPredictor.preprocessing(self.pokemon_data_df, const.LEGENDARY)

        print('test')


if __name__ == '__main__':
    pokemon_df = pd.read_csv('Pokemon.csv', index_col=1)  # index is pokemon name
    remove_cols = [const.ID, const.TYPE_1, const.TYPE_2, const.TOTAL]

    pokemon_df.drop(remove_cols, axis=1, inplace=True)

    x = LegendaryPredictor(pokemon_df)
    x()
