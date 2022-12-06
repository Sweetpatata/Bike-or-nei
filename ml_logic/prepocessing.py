import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, date, timezone
import glob
from sklearn.preprocessing import OneHotEncoder
from ml_logic.params import TARGET, input_length, output_length, N_TRAIN, N_TEST

def encode_day_month(X, col_list):
    ohe = OneHotEncoder(sparse = False)
    ohe.fit(X[col_list])
    X[ohe.get_feature_names_out()] = ohe.transform(X[col_list])
    return X.drop(columns = col_list)

def get_Xi_yi(
    fold,
    input_length,
    output_length):
    '''
    - given a fold, it returns one sequence (X_i, y_i)
    - with the starting point of the sequence being chosen at random
    '''
    first_possible_start = 0
    last_possible_start = len(fold) - (input_length + output_length) + 1
    random_start = np.random.randint(first_possible_start, last_possible_start)
    X_i = fold.iloc[random_start:random_start+input_length]
    y_i = fold.iloc[random_start+input_length:
                  random_start+input_length+output_length][[TARGET]]

    return (X_i, y_i)

def get_X_y(
    fold,
    number_of_sequences,
    input_length,
    output_length
    ):

    X, y = [], []

    for i in range(number_of_sequences):
        (Xi, yi) = get_Xi_yi(fold, input_length, output_length)
        X.append(Xi)
        y.append(yi)

    return np.array(X), np.array(y)

def get_train_test(df_dict):
    X_train_dict = {}
    y_train_dict = {}
    X_test_dict = {}
    y_test_dict = {}
    for station, df_station in df_dict.items():
        X_train, y_train = get_X_y(df_station, N_TRAIN, input_length, output_length)
        X_test, y_test = get_X_y(df_station, N_TEST, input_length, output_length)
        X_train_dict["X_train_{}".format(station)] = X_train
        y_train_dict["y_train_{}".format(station)] = y_train
        X_test_dict["X_test_{}".format(station)] = X_test
        y_test_dict["y_test_{}".format(station)] = y_test
    return X_train_dict, y_train_dict, X_test_dict, y_test_dict
