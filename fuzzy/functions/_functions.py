"""
Fuzzy functions are fuzzy logical functions.
"""
from abc import ABCMeta, abstractmethod


class FuzzyMembershipFunction(metaclass=ABCMeta):
    """
    Base class for membership functions in fuzzy logic.

    """
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
        assert min_full_boundary <= max_full_boundary
        if lower_boundary != float('-inf'):
            assert lower_boundary < min_full_boundary
        else:
            left_infinite_trapezoid = min_full_boundary == float('-inf')
            assert left_infinite_trapezoid

        if upper_boundary != float('inf'):
            assert max_full_boundary < upper_boundary
        else:
            right_infinite_trapezoid = max_full_boundary == float('inf')
            assert right_infinite_trapezoid

        self.lower_boundary = lower_boundary
        self.min_full_boundary = min_full_boundary
        self.max_full_boundary = max_full_boundary
        self.upper_boundary = upper_boundary

    def __call__(self, fuzzy_value: float) -> float:
        """TODO: TDD IT!"""


class InfiniteTrapezoidFunction(TrapezoidFunction):
    def __init__(
            self,
            left_vertex: float,
            right_vertex: float,
            infinite_side: str = 'left'
    ):
        assert infinite_side in ['left', 'right']
        assert float('-inf') < left_vertex < right_vertex < float('inf')

        lower_boundary = min_full_boundary = float('-inf')
        max_full_boundary = upper_boundary = float('inf')
        if infinite_side == 'left':
            max_full_boundary = left_vertex
            upper_boundary = right_vertex
        else:
            lower_boundary = left_vertex
            min_full_boundary = right_vertex

        super(InfiniteTrapezoidFunction, self).__init__(
            lower_boundary=lower_boundary,
            min_full_boundary=min_full_boundary,
            max_full_boundary=max_full_boundary,
            upper_boundary=upper_boundary
        )
