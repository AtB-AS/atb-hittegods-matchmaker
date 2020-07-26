# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 13:15:14 2020

@author: gauhol
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import Matching
import datetime
from dataset import Dataset

from utils import get_dataframe

"""

Generates random datasets for testing purposes

"""


def generate_random_datapoint(columns_and_possible_values, i):
    """
    Makes a random datapoint

    :param columns_and_possible_values: dataframe with columns with possible values for the column
    :param i: the row number for the datapoint to be generated
    :return: list of random values corresponding to one row
    """

    random_values = []
    column_names = list(columns_and_possible_values.columns)

    for colName in column_names:
        values = columns_and_possible_values[colName].tolist()
        values = remove_empty_from_list(values)
        random_value = generate_random_value(values)

        if colName == "foundid":
            random_values.append(i)

        elif colName == "date":
            date_arr = random_value.split("/")
            date = datetime.date(int(date_arr[2]), int(date_arr[1]), int(date_arr[1]))
            random_values.append(date)

        elif "id" in colName and colName != "lineid":
            value = int(random_value)
            random_values.append(value)

        else:
            random_values.append(random_value)

    return random_values


def generate_random_value(possible_values):
    """Returns a random values from the possible values"""
    max_len = len(possible_values)
    random_index = random.randint(0, max_len - 1)
    return possible_values[random_index]


def remove_empty_from_list(List):
    """Removes emppty values from the list of possible values"""
    new_list = []
    for item in List:
        if not pd.isna([item]):
            new_list.append(item)
    return new_list


def generate_randomDF(columns_and_possible_values, n):
    """
    Generates a pandas dataframe with random values from the possible values for each column

    :param columns_and_possible_values: dataframe with columns with possible values
    :param n: number of rows
    :return: random dataframe
    """
    column_names = list(columns_and_possible_values.columns)
    new_df_dict = {}
    for i in range(n):
        new_df_dict.update({str(i): generate_random_datapoint(columns_and_possible_values, i)})
    new_df = pd.DataFrame.from_dict(new_df_dict, orient="index", columns=column_names)
    return new_df


def generate_dataset(inputFile, outputFile, n):
    """
    Generates a random tab delimitered .txt file with column names as in the input file and random values from
    the possible values of each column in the input file.

    :param inputFile:
    :param outputFile:
    :param n: rows in output file
    """
    column_name_values = get_dataframe(inputFile)

    data_set = generate_randomDF(column_name_values, n)
    data_set.to_csv("Data/" + outputFile, sep="\t", index_label="foundid")


def test_matching():
    input_file = "Constants/ColumnsAndValuesData.txt"
    column_name_values = get_dataframe(input_file)

    data_set = generate_randomDF(column_name_values, 100)
    column_names = list(data_set.columns)
    x_column_names = column_names
    x_column_names.remove("foundid")
    x_column_names.insert(0, "lostid")

    x_values = list(dict(data_set.iloc[0]).values())
    x_dict = {x_column_names[i]: x_values[i] for i in range(len(x_column_names))}

    x = pd.DataFrame(x_dict, index=[0])
    
    x_dataset=Dataset('lost','single',x)
    y_dataset=Dataset('found','multiple',data_set)
    
    print(data_set.head())
    print(x.head())
    print(type(x))

    Matching.do_matching(x_dataset, y_dataset, 5)
