#!/usr/bin/env python3
# ------------------------------
# -*- coding: utf-8 -*-
#
# Name:     matrix.py
# Purpose:  Module that contains matrices and dataframe processing.
#
# @uthor:   acph - dragopoot@gmail.com
#
# Created:     May 2025
# Copyright:   (c) acph 2025
# Licence:     MIT
# ------------------------------
"""Module that contains matrices and dataframe processing."""


import numpy as np


def number_comparissons(x, diagonal=False):
    """Return the number of comparissons in a square matrix of len x.

    if diagonal == True , returns the number of comparissons in the complete matrix
    else , returns only the halve comparissons
    """
    if diagonal:
        return x**2
    else:
        y = (((x**2)-x)/2) + x
        return y


def list2matrix(id1, id2, values, dtype=np.float16, base_val=np.zeros, diagonal=True):
    """ Transform a set of 3 lists in a matrix. ids1, ids2, values must be the same lenght.

    The matrix must be N x N.

    Arguments:
    - `id1`: Identification number 1. numpy array
    - `id2`: Identification number 2. numpy array
    - `values`: Value of the cell i,j. numpy array
    - `dtype`: Numpy data type
    - `base_val`: numpy function to create "empty" matrix
    - `diagonal`: If True, the data only contains half matrix
    """
    n = id1.max()
    m = id2.max()
    N = np.max([n, m])
    minus = 1
    if id1.min() == 0 or id2.min() == 0:
        minus = 0
        N += 1
    mats = base_val((N, N), dtype=dtype)
    for d in range(len(id1)):
        i = id1[d] - minus
        j = id2[d] - minus
        val = values[d]
        mats[i,j] = val
        if diagonal == True:
            mats[j,i] = val
    return mats


def mat_percent_columns(matrix):
    """Normalize the column of a matrix dividing each element in a column by the sum of elements in a column, i.e. it calcules the percentage of each elemnten in a column

    Arguments:
    - `matrix`: a numpy 2d array
    """
    nmatrix = matrix.copy() # new matrix
    sums = matrix.sum(0)
    for i in range(len(matrix)):
        nmatrix[i] = matrix[i] / sums
    nmatrix[np.isnan(nmatrix)] = 0
    return nmatrix


def mat_percent_rows(matrix):
    """Normalize the rows of a matrix dividing each element in a row by the sum of elements in a row, i.e. it calcules the percentage of each elemnten in a row

    Arguments:
    - `matrix`:a numpy 2d array
    """
    nmatrix = matrix.copy()     # new matrix
    nmatrix = nmatrix.transpose()
    sums = nmatrix.sum(0)
    for i in range(len(nmatrix)):
        nmatrix[i] = nmatrix[i] / sums
    nmatrix = nmatrix.transpose()
    nmatrix[np.isnan(nmatrix)] = 0
    return nmatrix


def mat_max_rows(matrix):
    """Normalize the rows of a matrix dividing each element by the maximum value of each row

    Arguments:
    - `matrix`: a numpy 2d array
    """
    nmatrix = matrix.copy()
    nmatrix = nmatrix.transpose()
    maxs = nmatrix.max(0)
    for i in range(len(nmatrix)):
        nmatrix[i] = nmatrix[i] / maxs
    nmatrix = nmatrix.transpose()
    nmatrix[np.isnan(nmatrix)] = 0
    return nmatrix

def mat_other_rows(matrix, normalize_vals):
    """Normalize the rows of a matrix using a extra list of data

    Arguments:
    - `matrix`: a numpy 2d array
    - `normalize_vals`: a list of data to normalize, 1d numpy array
    """
    nmatrix = matrix.copy()
    nmatrix = nmatrix.transpose()
    for i in range(len(nmatrix)):
        nmatrix[i] = nmatrix[i] / normalize_vals
    nmatrix = nmatrix.transpose()
    nmatrix[np.isnan(nmatrix)] = 0
    return nmatrix
