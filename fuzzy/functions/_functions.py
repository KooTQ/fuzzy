"""
Fuzzy functions are fuzzy logical functions.
"""
from abc import ABCMeta, abstractmethod


class FuzzyMembershipFunction(metaclass=ABCMeta):
    """Base class for membership functions in fuzzy logic."""

    @abstractmethod
    def __call__(self, input_point: float) -> float:
        """Return fuzzy set membership value for a given input point.

        :param input_point: point in data-space
           to calculate membership degree for.
        :type input_point: float
        :return: fuzzy set membership degree in range[0;1]. Represents in what
           degree given input_point is member of fuzzy set.
        :rtype: float
        """
        pass


class TrapezoidFunction(FuzzyMembershipFunction):
    """Trapezoid Set Membership Function.

    TrapezoidFunction contains of 4 vertices:
       *. lower_boundary
       *. min_full_boundary
       *. max_full_boundary
       *. upper_boundary
    All data points of value lower or equal to lower_boundary have 0.
       membership degree. All data points of value greater or equal to
       upper_boundary have membership degree equal to 0. All data points
       of value greater or equal to min_full_boundary and lower or equal to
       max_full_boundary have membership degree equal to 1. All values between
       lower_boundary and min_full_boundary have membership degree equal to
       ```(value - lower_boundary)/(min_full_boundary - lower_boundary)```.
       And finally all values between max_full_boundary and upper_boundary
       have membership degree equal to
       ```(upper_boundary - value)/(upper_boundary - max_full_boundary)```.

    """
    lower_boundary: float
    """Left-most vertex."""
    min_full_boundary: float
    """Second-to-left vertex."""
    max_full_boundary: float
    """Third-to-left vertex."""
    upper_boundary: float
    """Right-most vertex."""

    def __init__(
            self,
            lower_boundary: float,
            min_full_boundary: float,
            max_full_boundary: float,
            upper_boundary: float,
    ) -> None:
        """

        :param lower_boundary:
        :param min_full_boundary:
        :param max_full_boundary:
        :param upper_boundary:
        """
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
        self._ascent_denominator = self.min_full_boundary - self.lower_boundary
        self._descent_denominator = self.upper_boundary - self.max_full_boundary

    def __call__(self, input_point: float) -> float:
        # Start plateau.
        if input_point <= self.lower_boundary:
            return 0.
        # Ascending slope.
        elif input_point < self.min_full_boundary:
            return (input_point - self.lower_boundary)/self._ascent_denominator
        # High plateau
        elif input_point < self.max_full_boundary:
            return 1.
        # Descending slope.
        elif input_point <= self.upper_boundary:
            return (self.upper_boundary - input_point)/self._descent_denominator
        # End plateau.
        return 0.


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
        self.infinite_side = infinite_side

    def __call__(self, input_point: float) -> float:
        """Pass input point to get membership degree.

        :param input_point: input to calculate membership degree
        :type input_point: float
        :return: membership degree.
        :rtype: float
        """
        if self.infinite_side == 'left':
            _input_point = max([input_point, self.max_full_boundary])
        else:
            _input_point = min([input_point, self.min_full_boundary])
        return super()(_input_point)


class TriangularFunction(TrapezoidFunction):
    def __init__(self, left: float, top: float, right: float):
        super().__init__(lower_boundary=left, min_full_boundary=top,
                         max_full_boundary=top, upper_boundary=right)
