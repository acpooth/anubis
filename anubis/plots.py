#!/usr/bin/env python3
#------------------------------
# -*- coding: utf-8 -*-
#
# Name:     plots.py
# Purpose:  General pourpose tools
#
# @uthor:   acph - dragopoot@gmail.com
#
# Created:     January 2012
# Copyright:   (c) acph 2012
# Licence:     MIT
#------------------------------
"""This module contains plot functions using matplotlib and seaborn and matplotlib tools"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def simple_bubble_plot(df, size_factor=25, xlabel='Columns',
                       cmap='Greys',
                       ylabel='Rows'):
    """Example of bubble plot, this function only works with small data, 0-10 approx,
    if color map is None, scatter use simple color"""
    n, m = df.shape
    X = df.values
    # here the processing for x
    X_ = X * size_factor
    alpha = X_/X_.max()
    # now the scatters plots, one for rows
    xs = range(m)
    for y in range(n):
        ys = [y] * m
        if cmap:
            plt.scatter(xs, ys,
                        c=alpha[y],
                        # c='steelblue',
                        cmap=cmap,
                        s=X_[y])
        else:
            plt.scatter(xs, ys,
                        c='steelblue',
                        s=X_[y])
    plt.xticks(np.arange(m), df.columns, rotation=90)
    plt.yticks(np.arange(n), df.index)
    plt.grid(linestyle=':', color='grey')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    return plt.gcf()


def percent_format(float_number, threshold=3):
    """ Format a percent float number to a round integer string if the value si superior to threshold, else, returns a empty string

    Arguments:
    - `float_number`: float number
    """
#    threshold = 3
    if float_number > threshold:
        num = '{}%'.format(int(round(float_number)))
    else:
        num = ''
    return num


def ax_letter(letter, ax):
    """Put the letter (or number) of a figure in the speficied axes
    the text is located in the uper left corner

    Arguments:
    - `letter`: Text to write
    - `axes`: Matplotlib axes object
    - `draggable`: Bool, if True, the text is draggable
    """
    text = plt.text(0.03, 0.97, letter, transform=ax.transAxes,
                    fontsize="xx-large", fontweight='bold', va='top')
    return text


def easy_pie(x, labels, threshold=3, explode=True, shadow=True, sort=True, colors=None):
    """   Function to easy create a pie chart that only shows the values and labels of the elements that has percentage values more than threshold. Returns the labels of the values that goes up to the rhreshold

    Arguments:
    - `x`: Array like colection of counts. Fractional area = x/sum(x)
    - `labels`: len(x) list of labels
    - `threshold`: Percentage threshold to show values
    - `explode`: None | If not None, len(x) array that contains the fraction to explode off the radius for each xi
    - `shadow`: False | True for show a shadow
    - `sort`: If true, sort the elements of the pie to get a better look
    - `colors`: list of colors for the color ring.  Default None: uses the default color ring
    """

    x = np.array(x, float)
    labels = np.array(labels)

    if sort == True:
        msort = np.argsort(x)
        x = x[msort]
        labels = labels[msort]


    mask  = (x/sum(x)*100) > threshold
    labels[ mask==0 ] = ''


    if explode == True:
        explode = np.zeros(len(x))
        explode[mask] = 0.2
    else:
        explode = None

    if colors is not None:
        assert np.iterable(colors), "colors argument is not iterable"
        colors = colors
    else:
        colors = ('b', 'g', 'r', 'c', 'm', 'y',  'w')

    formats = lambda n: percent_format(n, threshold)
#    plt.figure(figsize=(8,8))
#    ax = plt.axes([0.1, 0.1, 0.8, 0.8])
    plt.pie(x, labels=labels, autopct=formats , shadow=shadow, explode=explode, colors=colors)

    return labels[mask]


def axspan_gradient(axmin, axmax, spanmin=0, spanmax=1, direction='>',
                     alphafactor=0.005, spans=50, span='v', **kwargs):
    """Add a span (rectangle) across the axes in an alpha gradient
color.

Draw the vertical span with the same function as matplotlib. Creates n number
of spans in order to create the gradient effect. n = spans

    Arguments:
    - `axmin`: from x position
    - `axmax`: to x position
    - `spanmin`: from y position, default=0
    - `spanmin`: to y position, default=0
    - `direction`: Direction of the gradient [ '<' | '>' Default ]
    - `alphafactor`: alpha value used to each span, default=0.005
    - `spans`: number of components of the gradient, spans, default=25
    - `span`: Type of span, vertical or horizontal ['v' defautl | 'h']
    - **kwargs: kwargs for :class:`~matplotlib.patches.Polygon`
    """
    assert direction == '>' or direction == '<',\
        "Wrong direction flag. Accepted values [ '<' | '>' ]"
    assert span == 'v' or span == 'h',\
        "Wrong span flag. Accepted values [ 'v' | 'h' ]"
    if span == 'v':
        span = plt.axvspan
    elif span == 'h':
        span = plt.axhspan
    axs = np.linspace(axmin, axmax, spans)
    spans = []
    if direction == '>':
        for i in np.arange(1, len(axs)):
            _axmax = axs[i]
            ass = span(axmin, _axmax, spanmin, spanmax,
                              alpha=alphafactor, **kwargs)
            spans.append(ass)
    elif direction == '<':
        for i in np.arange(len(axs) - 1):
            _axmin = axs[i]
            ass = span(_axmin, axmax, spanmin, spanmax,
                              alpha=alphafactor, **kwargs)
            spans.append(ass)
    return spans
