"""
Fuzzy set membership functions calculate degree of membership for given value.

All function should be callable just like name implies.
"""
from abc import ABCMeta, abstractmethod


class FuzzyMembershipFunction(metaclass=ABCMeta):
    """Base class for membership functions in fuzzy logic."""

    @abstractmethod
    def __call__(self, input_point: float) -> float:
        """Return fuzzy set membership value for a given input point.

        :param input_point: point in data-space
           to calculate membership degree for.
        :return: fuzzy set membership degree in range[0;1]. Represents in what
           degree given input_point is member of fuzzy set.
        """
        pass


class TrapezoidFunction(FuzzyMembershipFunction):
    """
    Trapezoid Set Membership Function.

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
        Construct object base on all vertices.

        :param lower_boundary: Start of ascending slope;
          each input point value lower than lower_boundary will return 0.
        :param min_full_boundary: End of ascending slope;
          each input point value between min_full_boundary and max_full_boundary
          will return 1.
        :param max_full_boundary: Start of descending slope.
        :param upper_boundary: End of descending slope.
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
        """
        Pass input point to get membership degree.

        Each input_point in TrapezoidFunction can land on one of 5 places:
          *. Start plateau - return 0.
          *. Ascending slope - linear increase from 0. to 1.
          *. High plateau - return 1.
          *. Descending slope - linear decrease from 1. to 0.
          *. End plateau - return 0.

        :param input_point: input to calculate membership degree;
          value must be of type capable of being compared to vertices.
        :return: membership degree.
        """
        # Start plateau.
        if input_point <= self.lower_boundary:
            return 0.
        # Ascending slope.
        elif input_point < self.min_full_boundary:
            return (input_point - self.lower_boundary)/self._ascent_denominator
        # High plateau.
        elif input_point < self.max_full_boundary:
            return 1.
        # Descending slope.
        elif input_point <= self.upper_boundary:
            return (self.upper_boundary - input_point)/self._descent_denominator
        # End plateau.
        return 0.


class InfiniteTrapezoidFunction(TrapezoidFunction):
    """
    InfiniteTrapezoidFunction is TrapezoidFunction with infinite side.

    Infinite side can be either on left or on right. InfiniteTrapezoidFunction
      contains only 2 vertices:
        *. Left vertex
        *. Right vertex

    InfiniteTrapezoidFunction contains 3 distinguished parts:
      *. High plateau
      *. Low plateau
      *. Slope - either ascending or descending, start of slope is left vertex
        and end of slope is right vertex

    Examples of left InfiniteTrapezoidFunction:
    ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾\\_
    ‾‾‾‾‾‾‾‾\\________
    ‾\\_______________


    For left InfiniteTrapezoidFunction order of parts and vertices is:
      *. High plateau
      *. Left vertex (max full boundary)
      *. Descending slope
      *. Right vertex (upper boundary)
      *. Low plateau

    Examples of right InfiniteTrapezoidFunction:
    _____/‾‾‾‾‾
    _/‾‾‾‾‾‾‾‾‾
    _________/‾
    For right InfiniteTrapezoidFunction order of parts and vertices  is:
      *. Low plateau
      *. Left vertex (lower boundary)
      *. Ascending slope
      *. Right vertex (min upper boundary)
      *. High plateau
    """
    def __init__(
            self,
            left_vertex: float,
            right_vertex: float,
            infinite_side: str = 'left'
    ) -> None:
        """
        Construct trapezoid membership function based with single infinite side.

        :param left_vertex: Point of start of slope.
        :param right_vertex: Point of end of slope.
        :param infinite_side: Defining which side contains high plateau;
          possible values ```'left'``` and ```'right'```.
        """
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
        """
        Pass input point to get membership degree.

        Each input point can land on one of 3 places:
          *. High plateau - return 1.
          *. Low plateau - return 0.
          *. Slope - linearly descending/ascending values between 0. and 1.

        For left InfiniteTrapezoidFunction order of possible places is:
          *. High plateau
          *. Descending slope
          *. Low plateau

        For right InfiniteTrapezoidFunction order of possible places is:
          *. Low plateau
          *. Ascending slope
          *. High plateau

        :param input_point: input to calculate membership degree
        :return: membership degree.
        """
        if self.infinite_side == 'left':
            _input_point = max([input_point, self.max_full_boundary])
        else:
            _input_point = min([input_point, self.min_full_boundary])
        return super().__call__(_input_point)


class TriangularFunction(TrapezoidFunction):
    """
    TriangularFunction is membership trapezoid function without high plateau.

    Examples of TriangularFunction:
    _____/\\_____
    _/\\_________
    _________/\\_
    """
    def __init__(self, left: float, top: float, right: float):
        """
        Construct triangular membership function.
        :param left: End of start low plateau, start of ascending slope.
        :param top: End of ascending slope and start of descending slope.
        :param right: End of descending slope, start of end low plateau.
        """
        super().__init__(lower_boundary=left, min_full_boundary=top,
                         max_full_boundary=top, upper_boundary=right)
