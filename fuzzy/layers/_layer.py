"""
Implementation of fuzzy reasoning Layers.

Each layer is stack of multiple FuzzyRules.
"""
from typing import List, Dict, Tuple

import numpy as np

from fuzzy.functions import FuzzyMembershipFunction
from fuzzy.operators import Operatable


_DEF_NAMES = [
    'extremely low', 'very low', 'low', 'barely low',
    'moderate', 'barely high', 'high', 'very high',
    'extremely high'
]


DEFAULT_GRADES = {
    2: [_DEF_NAMES[2], _DEF_NAMES[6]],
    3: [_DEF_NAMES[2], _DEF_NAMES[4], _DEF_NAMES[6]],
    4: [_DEF_NAMES[1], _DEF_NAMES[2], _DEF_NAMES[6], _DEF_NAMES[7]],
    5: [_DEF_NAMES[1], _DEF_NAMES[2], _DEF_NAMES[4], _DEF_NAMES[6],
        _DEF_NAMES[7]],
    6: [_DEF_NAMES[1], _DEF_NAMES[2], _DEF_NAMES[3], _DEF_NAMES[5],
        _DEF_NAMES[6], _DEF_NAMES[7]],
    7: [_DEF_NAMES[1], _DEF_NAMES[2], _DEF_NAMES[3], _DEF_NAMES[4],
        _DEF_NAMES[5], _DEF_NAMES[6], _DEF_NAMES[7]],
    8: [_DEF_NAMES[0], _DEF_NAMES[1], _DEF_NAMES[2], _DEF_NAMES[3],
        _DEF_NAMES[5], _DEF_NAMES[6], _DEF_NAMES[7], _DEF_NAMES[8]],
    9: [_DEF_NAMES[0], _DEF_NAMES[1], _DEF_NAMES[2], _DEF_NAMES[3],
        _DEF_NAMES[4], _DEF_NAMES[5], _DEF_NAMES[6], _DEF_NAMES[7],
        _DEF_NAMES[8]]
}


class FuzzyLayer:
    """

    """
    functions: List[FuzzyMembershipFunction]
    """All functions in given domain, in same order as their predicates"""
    predicates: List[Operatable]
    """
    `Operatables` organized with all list of predicates for each FuzzyFunction
    """
    num_grades: int
    """Amount of fuzzy functions within domain."""
    domain_range: Tuple[float, float]
    """Range of expected values in domain."""

    def __init__(
            self,
            functions: List[FuzzyMembershipFunction],
            predicates: List[Operatable],
            domain_range: Tuple[float, float] = (0., 1.)
    ) -> None:
        """
        Initialize with given functions and predicates or with automatic

        :param functions: functions within domain
        :param predicates: predicates for given functions
        """
        assert len(functions) == len(predicates)
        self.num_grades = len(functions)
        self.domain_range = domain_range

    def estimate_center_of_mass(
            self,
            inputs: Dict[str, float],
            samplings: int = 100
    ) -> Tuple[float, float]:
        space = np.linspace(
            start=self.domain_range[0], stop=self.domain_range[1], num=samplings
        )
        width = (self.domain_range[1] - self.domain_range[0])
        delta = width / samplings
        domain_activations: List[List[float]] = [
            [] for _ in range(samplings)
        ]

        for i in range(len(self.functions)):
            cut_off_val = self.predicates[i](inputs)
            for val in space:
                if cut_off_val == 0:
                    domain_activations[val].append(0)
                else:
                    activation = self.functions[i](val)
                    domain_activations[val].append(max(activation, cut_off_val))
        full_domain = []
        sub_areas = []
        for activations in domain_activations:
            best_val = max(activations)
            full_domain.append(best_val)
            sub_areas.append(best_val * delta)
        area = sum(sub_areas)
        raise NotImplementedError()
#
