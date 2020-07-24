from csv import reader


def get_column_labels(lost=False, found=False):
    """
    Gets the column names from the ./Constants/columnLables.txt file determining which columns in the datasets are to
    be compared

    :param lost: True if dataset is lost
    :param found: True if dataset is found
    :return: column labels starting with lostid or foundid
    """

    file = open("Constants/columnLabels.txt", "r")
    labels = file.readline().split(",")
    if lost:
        labels.insert(0, "lostid")
    if found:
        labels.insert(0, "foundid")
    file.close()
    return labels


def get_value_labels():
    """
    Gets the column names of the values that are compared in the matching from ./Constants/columnLables.txt
    :return: column names of the values that are compared in the matching
    """

    file = open("Constants/columnLabels.txt", "r")
    labels = file.readline().split(",")
    file.close()
    return labels


def get_row_values(i, df, type):
    """
    Gets the row values to be compared from a pandas dataframe from the row number and column
    names in ./Constants/columnLables.txt

    :param i: row number
    :param df: pandas dataframe
    :param type: whether its lost or found data
    :return: row values to be compared from this dataframe
    """
    if type == "lost":
        labels = get_column_labels(lost=True)
    else:
        labels = get_column_labels(found=True)

    values = []
    for label in labels:
        values.append(df.loc[i, label])
    return values


def rename_contact_columns(df):
    """
    Renames the contact info columns where they differ in lost and found data so they are the same

    :param df: the pandas dataframe
    :return: pandas dataframe with correct column names
    """

    column_names = list(df.columns)
    for i in range(len(column_names)):
        if column_names[i] == 'nameonitem':
            column_names[i] = 'name'
        elif column_names[i] == 'phonenumberonitem':
            column_names[i] = 'phone'
        elif column_names[i] == 'emailonitem':
            column_names[i] = 'email'

    df.columns = column_names
    return df
