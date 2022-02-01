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
        """
        Estimate center of mass via quantized integral method.

        :param inputs: domain indexed measurements
        :param samplings: amount of quantized subdivisions
        :return: a pair of coordinates `(x, y)`
        """
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
            for j in range(len(space)):
                if cut_off_val == 0:
                    domain_activations[j].append(0)
                else:
                    activation = self.functions[i](space[j])
                    domain_activations[j].append(
                        min(activation, cut_off_val)
                    )
        area = 0.
        x_sub_value = 0.
        y_sub_value = 0.
        for activations, x in zip(domain_activations, space):
            best_val = max(activations)
            sub_area = best_val * delta
            area += sub_area
            x_sub_value += sub_area * x
            y_sub_value += sub_area * sub_area / 2
        if area > 0:
            x_coord = x_sub_value / area
            y_coord = y_sub_value / area
        else:
            x_coord = sum(self.domain_range) / 2
            y_coord = 0.
        return x_coord, y_coord
