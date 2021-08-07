"""
Fuzzy functions are fuzzy logical functions.
"""
from abc import ABCMeta, abstractmethod


class FuzzyMembershipFunction(metaclass=ABCMeta):
    @abstractmethod
    def __call__(self, fuzzy_value: float) -> float:
        pass


class TrapezoidFunction(FuzzyMembershipFunction):
    lower_boundary: float
    min_full_boundary: float
    max_full_boundary: float
    upper_boundary: float

    def __init__(
            self,
            lower_boundary: float,
            min_full_boundary: float,
            max_full_boundary: float,
            upper_boundary: float,
    ) -> None:
        assert lower_boundary < min_full_boundary < \
               max_full_boundary < upper_boundary

        self.lower_boundary= lower_boundary
        self.min_full_boundary = min_full_boundary
        self.max_full_boundary = max_full_boundary
        self.upper_boundary = upper_boundary

    def __call__(self, fuzzy_value: float) -> float:
        """TODO: TDD IT!"""
