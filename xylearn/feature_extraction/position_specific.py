# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 09:32:10 2018

@author: misakawa
"""

import numpy  as np
import pandas as pd
import numba as nb

from sklearn.preprocessing import normalize
from typing import List


@nb.jit
def count_ps_matrix(
        sequences: np.ndarray,
        bin_targets: np.ndarray,
        ps_matrix: np.ndarray,
        categories: tuple):
    for tag, sequence in zip(bin_targets, sequences):
        for idx, e in enumerate(sequence):
            ps_matrix[tag, categories.index(e), idx] += 1


class Method:
    @staticmethod
    def position_specific(stats: np.ndarray):
        return normalize(stats[1], axis=0) - normalize(stats[0], axis=0)

    @staticmethod
    def bi_profile(stats: np.ndarray):
        return np.hstack(
            (normalize(stats[1], axis=0), normalize(stats[0], axis=0)))


def represent(sequences: np.ndarray,
              bin_targets: np.ndarray,
              categories: tuple,
              *methods: tuple) -> List[pd.DataFrame]:
    assert all(map(lambda e: e in (0, 1), bin_targets))

    if not isinstance(categories, tuple):
        categories = tuple(categories)

    num, seq_length = sequences.shape
    psm = np.zeros((2, len(categories), seq_length), dtype=np.int64)

    # side effects
    count_ps_matrix(sequences, bin_targets, psm, categories)

    return [pd.DataFrame(method(psm), index=categories) for method in methods]
