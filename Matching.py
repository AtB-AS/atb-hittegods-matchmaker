# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 15:36:15 2020

@author: gauhol
"""
from collections import OrderedDict
from operator import itemgetter
import columns
import compare
import Weights
from Match import Match
from Entry import Entry

"""

Calling do_matching will initiate all the function calls to do do the matching for one entry x in a dataset y. 

The specific comparison functions are found in compare.py

Weights are found in Weights.py

"""


def do_matching(x, data, n):
    """
    Finds the n best matches of x in the dataset data

    Column names in df for values that are compared must be the same in x and data
    Corrections of columns etc are done in this function before the matching is done

    :param x: single entry data of type dataset
    :param data: multiple entry data of type dataset
    :param n: length of list of best matches
    :return: best n matches
    """

    # Corrects naming difference for contact info
    if x.lost_or_found == 'found':
        x.df = columns.rename_contact_columns(x.df)
    else:
        data.df = columns.rename_contact_columns(data.df)

    matches=matching(x, data, n)

    return matches


def matching(x_dataset, y_dataset, n):
    """
    Loops through all values in y_dataset and compares to the single entry in x_dataset. The best matches are returned

    Only the values in columns with names in ./Constants/columnLables.txt will be compared. The weights for the
    calculation are found in ./Constants/weightMatrix.txt
    :param x_dataset: single entry data of type dataset
    :param y_dataset: multiple entry data of type dataset
    :param n: length of list of best matches
    :return: best n matches
    """

    weight_matrix = Weights.get_weight_matrix()
    value_labels = columns.get_value_labels()

    x_row = columns.get_row_values(0, x_dataset.df, x_dataset.lost_or_found)
    x = Entry(x_row[0],x_row.remove(x_row[0]))

    scores = []
    y_ids = []
    print(len(y_dataset.df))
    for i in range(len(y_dataset.df)):
        y_row = columns.get_row_values(i, y_dataset.df, y_dataset.lost_or_found)

        y = Entry(y_row[0],y_row.remove(y_row[0]))
        print(y)
        try:
            scores.append(round(calculate_score(weight_matrix, compare_entries(x.values, y.values, value_labels)), 3))
            y_ids.append(y.id)
        except Exception as e:
            print(e)


    # This is where the bug happens
    [bestMatches, bestScores] = find_best_matches(scores, y_ids, n)

    matches = []
    for i in range(0, len(bestMatches)):
        if x_dataset.lost_or_found == "lost":
            matches.append(Match(x.id, bestMatches[i], bestScores[i]))
        else:
            matches.append(Match(bestMatches[i], x.id, bestScores[i]))

    return matches


def find_best_matches(s, id, n):
    """
    Finds best matches of all the similarity scores calculated

    :param s: scores
    :param id: id of y values
    :param n: how many of the best matches to return
    :return: y_ids and scores for best matches
    """
    refS = {id[i]: s[i] for i in range(len(id))}
    sortedRefS = OrderedDict(sorted(refS.items(), key=itemgetter(1), reverse=True))
    sortedRef = list(sortedRefS.keys())
    sortedS = list(sortedRefS.values())
    bestMatches = [sortedRef[i] for i in range(n)]
    bestS = [sortedS[i] for i in range(n)]

    return [bestMatches,bestS]


def calculate_score(weight_matrix, values):
    """
    Performs the weighted sum of all the comparison values, finding the final similarity score for entries x and y.

    The weights are calculated dynamically and will be different each time this function is called, depending on the
    input comparison values. The score will always be between -1 and 1.

    :param weight_matrix: The weight matrix constant
    :param values: the comparison values for the parameters from an entry in x and y
    :return: similarity score
    """

    weights = Weights.calculate_weights(values, weight_matrix)
    weighted_values = apply_weights(weights, values)

    top = 0
    bottom = 0
    for i in range(len(weighted_values)):
        top += weighted_values[i]
        bottom += max(abs(weights[i]), abs(weighted_values[i]))

    s = top / bottom
    return s


def compare_entries(x, y, labels):
    """
    Compares each value from an entry(row) in x and y. Returns a list of comparison values between 0 and 1 for each
    parameter

    :param x: list of row values in x
    :param y: list of row values in y
    :param labels: label for each corresponding parameter in x and y
    :return: comparison values for each parameter in x and y
    """
    values=[]
    for i in range(len(x)):
        values.append(compare_value(x[i], y[i], labels[i]))
    return values


def compare_value(x, y, label):
    """
    Compares the value of x and y with the corresponding compare function in compare.py according to the label

    :return: similarity score
    """
    return compare.compare(x, y, label)


def apply_weights(weights, values):
    """
    Applies the weight for each value

    :param weights: list of weights
    :param values: list of values
    :return: list of weighted values
    """
    weighted_values = []
    for i in range(len(values)):
        weighted_values.append(weights[i]*values[i])
    return weighted_values
