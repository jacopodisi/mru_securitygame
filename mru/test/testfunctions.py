import numpy as np


def compare_row_mat(x_mat, y_mat):
    """ Compare rows of 2, unordered, matrices
    Parameter
    ---------
    x_mat: 1st matrix to compare
    y_mat: 2nd matrix to compare

    Return
    ------
    boolean: True if the 2 matrices contains the same rows
             (also in different order), False otherwise
    """
    x_temp = np.unique(x_mat, axis=0)
    y_temp = np.unique(y_mat, axis=0)
    if x_temp.shape[0] != y_temp.shape[0]:
        return False
    for x in x_temp:
        if not np.any(np.all(x == y_temp, axis=1)):
            return False
    return True
