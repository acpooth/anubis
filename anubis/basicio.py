#!/usr/bin/env python3
#------------------------------
# -*- coding: utf-8 -*-
#
# Name:     basicio.py
# Purpose:  Module that contains IO functions
#
# @uthor:   acph - dragopoot@gmail.com
#
# Created:     May 2025
# Copyright:   (c) acph 2025
# Licence:     MIT
#------------------------------
"""Module that contains IO functions"""

import matplotlib.pyplot as plt
import numpy as np


def load_listdict(filename, sep=' ', single=False):
    """Loads a file into a python dictionary
    
    Arguments:
    - `filename`: The file name(path) the file must contain the folowing structure:
        * each line is a element of the dictionary
        * the first word is the key
        * following by a \t
        * next the elements corresponding to the value separated by 'sep'
    - `sep`: separator of the elements in the list
    - `single`: If sigle == True, the list file will be trated as a single dictionary, one key > one value.
        If False, the function asumes a the dictionary includes many values sep separated per key
    """
    dictionary = {}
    with open(filename, 'r') as inf:
        for line in inf:
            line = line.strip()
            if line == '' : continue
            line = line.split('\t')
            k = line[0]
            if single == True:
                v = line[1]
            else:
                v = line[1].split(' ')
            dictionary[k] = v
    return dictionary


def save_matrix(fname, matrix, headers, rownames, delimiter='\t'):
    """Create a text file with the matrix.

    Arguments:
    - `fname`: file name
    - `matrix`: array like 2d matrix
    - `headers`: first row that descrives each data column
    - `rownames`: first column that descrives each data row
    - `delimiter`: delimiter
    """

    with open(fname, 'w') as outf:
        head = delimiter.join(headers)
        head = delimiter + head + '\n'
        outf.write(head)
        for i, v in enumerate(rownames):
            data = [str(d) for d in matrix[i]]
            line = v + delimiter + delimiter.join(data) + '\n'
            outf.write(line)


def load_matrix(fname, delimiter='\t', header_lines=1, rowname_cols=1, datatype=np.float32):
    """This function loads a matrix text file, it may take into account more than one headers or row names.
The function returns three lists. A list of headers, a list of row names, and numpy array containing the matrix

    Arguments:
    - `fname`: file name
    - `delimiter`: delimiter
    - `header_lines`: Number of lines that contains headers
    - `rowname_cols`: Number of columns that contains row_names
    - `datatype`: Numpy data type to load data
    """
    with open(fname) as inf:
        lines = inf.read()
        lines = lines.split('\n')
        lines = [l.split(delimiter) for l in lines if l != '']
        headers = np.array(lines[:header_lines])
        lines = np.array(lines[header_lines:])
        rownames = lines[:, :rowname_cols]
        data = lines[:, rowname_cols:]
        data = data.astype(datatype)
    if len(headers) == 1:
        headers = headers[0]
    if len(rownames[0]) == 1:
        rownames = rownames[:,0]
    headers = headers[1:]
    return headers, rownames, data
