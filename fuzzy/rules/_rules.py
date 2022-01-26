"""
Implementation of fuzzy rules.
"""
from typing import Dict

from fuzzy.operators import Operatable
from fuzzy.functions import FuzzyMembershipFunction


class FuzzyRule:
    """
    FuzzyRule is implementation of fuzzy \'IF A THEN B\' statements.
    """
    operation: Operatable
    """Operation which result will point to functions activation."""
    function: FuzzyMembershipFunction
    """Function pointed to by operation."""
    activation: float
    """Maximal amount of activating function."""

    def __call__(
            self,
            inputs: Dict[str, float]
    ) -> float:
        """
        Calculate maximal activation of considered function based on its rule.
        :param inputs: dictionary containing domain values
        :return: functions activation cut-off
        """
        self.activation = self.operation(inputs)
        return self.activation
