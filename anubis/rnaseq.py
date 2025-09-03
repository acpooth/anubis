#!/usr/bin/env python3
#------------------------------
# -*- coding: utf-8 -*-
#
# Name:     rnaseq.py
# Purpose:  Tools for RNA-seq analysis
#
# @uthor:   acph - dragopoot@gmail.com
#
# Created:     January 2025
# Copyright:   (c) acph 2025
# Licence:     MIT
#------------------------------
"""Tools for RNA-seq analysis"""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# from matplotlib_venn import venn3


def volcano(df, title=None, loc=2, show_top=0):
    """Create a volcano plot from a snakePipes RNAseq DE result.

    Arguments:
    ---------
    show_top: int, [0]
         Show the specified number of top p value genes UP regulated
         and DOWN regulated genes
    """
    down = df.Status == 'DOWN'
    up = df.Status == 'UP'
    noDE = df.Status.isnull()

    plt.scatter(df.log2FoldChange[up],
                -np.log(df.padj[up]),
                s=10, c='g', alpha=0.5,
                label=f'Up: {up.sum()}')
    plt.scatter(df.log2FoldChange[noDE],
                -np.log(df.padj[noDE]),
                s=10, c='grey', alpha=0.3,
                label=f'No DE: {noDE.sum()}')
    plt.scatter(df.log2FoldChange[down],
                -np.log(df.padj[down]),
                s=10, c='r', alpha=0.5,
                label=f'Down: {down.sum()}')

    plt.xlabel('log2(FoldChange)')
    plt.ylabel("-log10(adj p-value)")
    plt.legend(loc=loc, fontsize='x-small')

    if title:
        plt.title(title)

    if show_top:
        for _gene, _data in df.query("Status == 'UP'").sort_values('padj').head(show_top).iterrows():
            x = _data.log2FoldChange
            y = -np.log(_data.padj)
            plt.annotate(_data['external_gene_name'], xy=(x,y), fontsize='xx-small', color='darkgrey')

        for _gene, _data in df.query("Status == 'DOWN'").sort_values('padj').head(show_top).iterrows():
            x = _data.log2FoldChange
            y = -np.log(_data.padj)
            plt.annotate(_data['external_gene_name'], xy=(x,y), fontsize='xx-small', color='darkgrey')


def plotPCA(countMatrix, groups=None, figsize=(6, 3), s=50):
    """Plot RNA-seq PCA.

    groups
    """
    scaler = StandardScaler()
    pca = PCA()
    X_std = scaler.fit_transform(countMatrix.T)
    X_pca = pca.fit_transform(X_std)

    dfpca = pd.DataFrame(X_pca, index=countMatrix.columns)

    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(121)

    axlegend = fig.add_subplot(122)
    # PCA
    sns.scatterplot(dfpca, y=1, x=0, hue=groups,
                    s=s,
                    style=dfpca.index, ax=ax)

    ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.0%})')
    ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.0%})')
    ax.axhline(ls=':', c='grey')
    ax.axvline(ls=':', c='grey')
    ax.legend_.set_visible(False)

    if not groups is None:
        handles = ax.get_legend_handles_labels()
        ng = len(set(groups))
        h1 = handles[0][:ng]
        lab1 = handles[1][:ng]
        h2 = handles[0][ng:]
        lab2 = handles[1][ng:]
        leg1 = axlegend.legend(h2, lab2, loc=2, title='Samples', frameon=False)
        leg2 = axlegend.legend(h1, lab1, loc=9, title='Groups', frameon=False)
        axlegend.add_artist(leg1)
    else:
        axlegend.legend(*ax.get_legend_handles_labels(), loc=2, title='Sample',
                        frameon=False)
    axlegend.axis('off')
    plt.tight_layout()


def get_DEgenes(df):
    """Get the UP and DOWN regulated genes from a DE dataframe.

    Arguments:
    df -- DataFrame
    """
    down = np.array(df.index[df.Status == 'DOWN'])
    up = np.array(df.index[df.Status == 'UP'])
    return {'down': down, 'up':up}


def read_DEfolders(pathlist, expnames):
    """Reads a list of snakePipes DE folders and return a dictionary
    matrices and DErsults

    Arguments:
    - pathlist, list
       List of DE directories
    - expnames, list
       List of experiment names

    Return:
    - A dictionary :P

    """
    data = {}
    for path, name in zip(pathlist, expnames):
        path = Path(path)
        data[name] = {"de": pd.read_table(next(path.glob("*results.tsv")),
                                          index_col=0),
                      "counts": pd.read_table(next(path.glob("*counts*normalized*")),
                                              index_col=0)
                      }
    return data
