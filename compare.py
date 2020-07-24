# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 14:41:35 2020

@author: gauhol
"""

import datetime
import math
import numpy as np


def compare(x, y, label):
    """Determines how similar x and y are using the corresponding comparison function for its label

    Will return 0 if:
        -There is no corresponding comparison for the label
        -x or y is none
        -x and y is determined to not be similar at all

    :param x: to be compared with y
    :param y: tp be compared with x
    :param label: the type of data for x and y
    :return: a similarity value between 0 and 1
    """

    if x is None or y is None:
        return 0

    if x is "" or y is "":
        return 0

    if label == "catid" or label == "subcatid" or label == "colorid":
        if str(x).isdigit() and str(y).isdigit():
            return compare_id(x, y)

    elif label == 'phone':
        if str(x).isdigit() and str(x).isdigit() and min(len(x),len(y))>0:
            return compare_phone(x, y)

    elif label == 'email':
        if check_type(x, y, str, label) and '@' in x and '@' in y and  min(len(x), len(y))>0:
            return compare_email(x, y)

    elif label == "lineid":
        if str(x).isdigit():
            x = str(x)
        if str(y).isdigit():
            y = str(y)

        if check_type(x, y, str, label):
            return compare_line(x, y)

    elif label == "brand" or label == 'name':
        if check_type(x, y, str, label) and min(len(x), len(y))>0:
            return compare_brand(x, y)

    elif label == "date":
        if check_type(x, y, datetime.date, label):
            return compare_date(x, y)

    elif label == "description":
        if check_type(x, y, str, label) and min(len(x), len(y))>0:
            return compare_description(x, y)

    return 0


def check_type(x, y, the_type, label):
    """
    Determines whether x and y is of the correct type

    :param x:
    :param y:
    :param the_type:
    :param label:
    :return: True if correct type, False otherwise
    """
    if type(x) == the_type and type(y) == the_type and x != None:
        return True
    else:
        print("wrong type" + str(type(x)) + str(type(y)) + " for " + label)
        return False


def compare_description(x, y):
    """
    Finds the amount of similar words there are in two descriptions and calculates a similarity score

    The score is calculated using a logarithms to try to get similar values regardless of
    the length of the sentences. The returned value is probabilistic

    :param x: description 1
    :param y: description 2
    :return: similarity score
    """

    same_word, n_words = compare_words(x, y, return_num_words=True)

    N = n_words[0] * n_words[1]

    similarity = (same_word / math.log(1 + N)) ** (abs(math.log(N / 2)))

    return min(similarity, 1)


def compare_phone(x, y):
    """
    Compares two phone numbers. Also makes sure one the phone numbers are approximately the same length
    :param x: phone number 1
    :param y:   phone number 2
    :return: similarity score
    """
    x = remove_spaces(x)
    y = remove_spaces(y)

    if (x in y or y in x) and (min(len(x), len(y)) > 0.7*max(len(x), len(y))):
        return 1
    else:
        return 0


def compare_email(x_email, y_email):
    """
    Compares two emails. Also makes sure one the emails are approximately the same length
    :param x_email: email 1
    :param y_email:   email 2
    :return: similarity score
    """
    if (x_email in y_email or y_email in x_email) and (min(len(x_email), len(y_email)) > 0.7 * max(len(x_email), len(y_email))):
        return 1
    else:
        return 0


def compare_date(x_date, y_date):
    """
    Finds the number of days between date 1 and date 2

    :param x_date:
    :param y_date:
    :return: similarity score
    """

    if type(x_date) != datetime.date or type(y_date) != datetime.date:
        print("WARNING: Date not type datetime.date")
        return 0

    # Assuming type datetime.date

    timedelta = abs((x_date - y_date).days)

    if timedelta < 3:
        return 1

    return 2 / timedelta


def compare_id(x_id, y_id):
    """
    Checks if an int is the same as another int. Used for color id, category id etc

    :return: similarity score
    """
    if x_id == y_id:
        return 1
    else:
        return 0


def compare_line(x_line, y_line):
    """
    Checks if a line in list x is in list y

    :return: similarity score
    """
    sameLine = 0

    x_arr = split_words(x_line, [",", ".", ":", ";"])
    y_arr = split_words(y_line, [",", ".", ":", ";"])

    for line_x in x_arr:
        for line_y in y_arr:
            if line_x == line_y:
                sameLine += 1

    # Should this be evaluated differently
    if sameLine > 0:
        return 1
    else:
        return 0


def compare_brand(x_brand, y_brand):
    """
    Checks if the same word occurs in both x and y

    :return: similarity score"""

    same_word = compare_words(x_brand, y_brand)

    if same_word > 0:
        return 1
    else:
        return 0


def compare_words(x_string, y_string, return_num_words=False):
    """
    Checks how many words occur in both x and y

    :param x_string: x sentence
    :param y_string: y sentence
    :param return_num_words: whether the word count in sentence x and y is returned
    :return: how many times the same word occured in x and y
    """

    treshold = 0.6
    same_word = 0
    x_arr = split_words(x_string, [",", ".", ":", ";"])
    y_arr = split_words(y_string, [",", ".", ":", ";"])

    for word_x in x_arr:
        for word_y in y_arr:
            if compare_char_array(word_x, word_y) > treshold:
                same_word += 1
    if return_num_words:
        return [same_word, [len(x_arr), len(y_arr)]]
    else:
        return same_word


def split_words(sentence, delimeters):
    """Splits sentence into words by delimeters, list of words"""
    for delimeter in delimeters:
        sentence = sentence.replace(delimeter, " ")
    word_arr = sentence.split(" ")
    return word_arr


def remove_spaces(string_with_spaces):
    """Removes spaces in a string"""
    x_arr = list(string_with_spaces)
    while " " in x_arr:
        x_arr.remove(" ")
    x_str = ""
    return x_str.join(x_arr)


def compare_char_array(x_word, y_word):
    """
    Compares two strings, tries to determine whether it's the same word in x and y

    :return: similarity score
    """
    
    if x_word == '' or y_word == '':
        return 0
    else:
        same_char = 0
        x_word = x_word.lower()
        y_word = y_word.lower()
        x_arr = list(x_word)
        y_arr = list(y_word)
    
        for char_x in x_arr:
            if char_x.isdigit():
                continue
            for char_y in y_arr:
                if char_y.isdigit():
                    continue
                elif char_x == char_y:
                    same_char += 1
    
        return same_char / max([len(x_arr), len(y_arr)])
