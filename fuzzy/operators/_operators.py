"""
Operators on fuzzy membership functions.
"""
from abc import ABC, abstractmethod
from typing import Union, List

from functions import FuzzyMembershipFunction

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
