# My python implementation of https://towardsdatascience.com/introduction-to-machine-learning-with-pokemon-ccb7c9d1351b
# CSV data taken from: https://drive.google.com/file/d/1nUwdfPHiqXmz8Zh89SxPSiIFwbm9IOvv/view
# Reference: https://towardsdatascience.com/building-a-logistic-regression-in-python-step-by-step-becd4d56c9c8

import pandas as pd
from imblearn.over_sampling import SMOTE
import machine_learning.constant as const
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import RFE
from itertools import compress
import statsmodels.api as sm
from sklearn import metrics
import matplotlib.pyplot as plt


# todo this didn't need to be a class, right now it's all just static methods.  Think about this more.

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

    @staticmethod
    def recursive_feature_elimination(X_os_data, y_os_data):
        """
        Use recursive feature elimination to select the best 4 features to use, using logistic regression as the
        estimator

        Args:
            X_os_data: <pd.DataFrame> X trained data
            y_os_data: <pd.DataFrame> y trained data

        Returns: <list> of the chosen features to use resulting from rfe

        """
        rfe = RFE(LogisticRegression(), n_features_to_select=4)
        rfe = rfe.fit(X_os_data, y_os_data.values.ravel())
        chosen_features = list(compress(X_os_data.columns, rfe.support_))

        return chosen_features

    @staticmethod
    def run_logistic_model(X_os_data, y_os_data):
        model = sm.Logit(y_os_data, X_os_data)
        result = model.fit()

        # print(result.summary2())

        # Logistical Regression Model Fitting
        X_train, X_test, y_train, y_test = train_test_split(X_os_data, y_os_data, test_size=0.25, random_state=0)
        log_reg_model = LogisticRegression()
        log_reg_model.fit(X_train, y_train.values.ravel())

        # Predict results
        y_predict = log_reg_model.predict(X_test)

        # ROC Curve
        log_reg_roc_auc = metrics.roc_auc_score(y_test, y_predict)
        false_pos, true_pos, thresh = metrics.roc_curve(y_test, log_reg_model.predict_proba(X_test)[:, 1])

        plt.figure()

        # Our ROC plot (receiver operating characteristic)
        plt.plot(false_pos, true_pos, label='Model ROC (area = {})'.format(round(log_reg_roc_auc, 2)))

        # ROC of purely random classifier
        plt.plot([0, 1], [0, 1])

        plt.title('Pokemon Predicting Legendary ROC Curve')
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.legend()

        plt.savefig('Pokemon Predicting Legendary ROC Curve.png')
        plt.show()

        # some metrics
        dict_results = {'acc_on_test_set': log_reg_model.score(X_test, y_test),
                        'confusion_matrix': metrics.confusion_matrix(y_test, y_predict)}

        return dict_results

    def __call__(self):
        X_os_data, y_os_data = LegendaryPredictor.preprocessing(self.pokemon_data_df, const.LEGENDARY)
        rfe_chosen_feature = LegendaryPredictor.recursive_feature_elimination(X_os_data, y_os_data)

        # only include the chosen features in the actual model
        X_os_data = X_os_data[rfe_chosen_feature]
        logit_model_results = LegendaryPredictor.run_logistic_model(X_os_data, y_os_data)


if __name__ == '__main__':
    pokemon_df = pd.read_csv('Pokemon.csv', index_col=1)  # index is pokemon name
    remove_cols = [const.ID, const.TYPE_1, const.TYPE_2, const.TOTAL]

    pokemon_df.drop(remove_cols, axis=1, inplace=True)

    x = LegendaryPredictor(pokemon_df)
    x()
