"""
Operators on fuzzy membership functions.
"""
from abc import ABC, abstractmethod
from typing import Union, List

from fuzzy.functions import FuzzyMembershipFunction

Operatable = Union[FuzzyMembershipFunction, "FuzzyOperator"]


class FuzzyOperator(ABC):
    """
    Base class for FuzzyOperators for combining FuzzyMembershipFunctions 
      and other FuzzyOperators into single complex callable pipeline.
    """
    
    functions: List[Operatable]
    """
    Contains FuzzyMembershipFunctions and FuzzyOperators to apply operation on.
    """

    def __init__(
            self,
            *functions: Operatable
    ) -> None:
        """
        FuzzyOperator requires fuzzy membership functions to operate on.

        :param functions: Iterator of FuzzyMembershipFunction or FuzzyOperator
          objects to apply operator on; in case of single argument operators,
          functions iterator should contain only one object
        """
        self.functions = list(functions)

    @abstractmethod
    def __call__(
            self,
            value: float
    ) -> float:
        """
        Call pipeline of in self.functions and apply on result operator.
        
        :param value: value to pass through FuzzyMembershipFunctions
        :return: result of pipeline
        """

class TNorm(FuzzyOperator):
    """
    Intersection of fuzzy sets.

    Could be read as "AND" operator.
    """

    def __call__(self, value: float) -> float:
        results = []
        for ff in self.functions:
            res = ff(value)
            if res == 0:
                return 0.
            results.append(res)
        return min(results)


class SNorm(FuzzyOperator):
    """
    Union of fuzzy sets.

    Could be read as "OR" operator.
    """

    def __call__(self, value: float) -> float:
        """
        Pass through fuzzy function and negate option.

        :param value: value to calculate negation on given function
        :return: negated degree of membership
        """
        results = []
        for ff in self.functions:
            res = ff(value)
            if res == 1:
                return 1.
            results.append(res)
        return max(results)


class StrongNegation(FuzzyOperator):
    """
    Negates scale of membership degree.

    Could be read as "NOT" operator.
    """
    def __init__(
            self,
            function: Operatable
    ) -> None:
        """
        Create negation for given Operatable object.

        :param function: can be either FuzzyMembershipFunction or
          FuzzyOperator
        """
        super().__init__(function)

    def __call__(self, value: float) -> float:
        """
        Pass through fuzzy function and negate option.

        :param value: value to calculate negation on given function
        :return: negated degree of membership
        """
        return 1 - self.functions[0](value)
