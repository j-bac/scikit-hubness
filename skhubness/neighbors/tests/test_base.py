# SPDX-License-Identifier: BSD-3-Clause

import pytest
from skhubness.neighbors.base import NeighborsBase, ANN_ALG
from skhubness.reduction import hubness_algorithms, hubness_algorithms_long


@pytest.mark.parametrize('algo', hubness_algorithms + hubness_algorithms_long)
def test_check_hubness_accepts_valid_values(algo):
    NeighborsBase(hubness=algo)._check_hubness_algorithm()


@pytest.mark.parametrize('algo', ['auto', 'brute', 'kd_tree', 'ball_tree'] + ANN_ALG)
def test_check_algorithm_accepts_valid_values(algo):
    NeighborsBase(algorithm=algo)._check_algorithm_metric()