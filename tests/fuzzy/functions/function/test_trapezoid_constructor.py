"""
Unit tests TrapezoidFunction.__init__:
  1. set in constructor *lower_boundary* with higher than *upper_boundary*
  1. set in constructor *min_full_boundary* with higher than *upper_boundary*
  1. set in constructor *max_full_boundary* with higher than *upper_boundary*
  1. set in constructor *lower_boundary* with higher than *max_full_boundary*
  1. set in constructor *min_full_boundary* with higher than *max_full_boundary* 
  1. set in constructor *lower_boundary* with higher than *min_full_boundary*
"""

import pytest

from fuzzy.functions import (
    TrapezoidFunction, InfiniteTrapezoidFunction, TriangularFunction
)


def test_typical_trapezoid_membership_objects() -> None:
    # Typical trapezoid membership functions - with start, end, ascending slope,
    #  plateau and descending slope. ___/‾\_ or _/‾\___ or _/‾‾‾‾\_ or similar.
    t = TrapezoidFunction(0., 1., 2., 3.)
    assert isinstance(t, TrapezoidFunction)
    t = TrapezoidFunction(-1., 0.1, 0.11, 5.)
    assert isinstance(t, TrapezoidFunction)


def test_infinite_trapezoid_membership_function_objects() -> None:
    t0 = InfiniteTrapezoidFunction(0, 1)
    assert isinstance(t0, InfiniteTrapezoidFunction)


def test_wrong_infinite_trapezoid_membership_function_objects() -> None:
    # Infinity should be either on both vertices of ascending slope
    #  or on both vertices of descending slope.
    pytest.raises(AssertionError, TrapezoidFunction,
                  float('-inf'), 0., 1., 2)
    pytest.raises(AssertionError, TrapezoidFunction,
                  -1, 0., 1., float('inf'))

    # There can be only one inf
    pytest.raises(AssertionError, TrapezoidFunction,
                  float('-inf'), 0., 1., float('inf'))
    pytest.raises(AssertionError, TrapezoidFunction,
                  float('-inf'), 0., 1., float('inf'))


def test_wrong_vertices_values() -> None:
    pytest.raises(AssertionError, TrapezoidFunction, 0., -1., 2., 3.)
    pytest.raises(AssertionError, TrapezoidFunction, 0., 1., -1., 3.)
    pytest.raises(AssertionError, TrapezoidFunction, 0., 1., 2., -1.)

    pytest.raises(AssertionError, TrapezoidFunction, 0., 1., 0.5, 3.)
    pytest.raises(AssertionError, TrapezoidFunction, 0., 1., 2., 0.5)

    pytest.raises(AssertionError, TrapezoidFunction, 0., 1., 2., 1.5)
    pytest.raises(AssertionError, TrapezoidFunction, 0., 1., 2., -1.)

    pytest.raises(AssertionError, TrapezoidFunction, 0., 0., 0., 0.)


def test_triangular_constructor_good_values() -> None:
    # Sanity checks
    triangular_function = TriangularFunction(-100, 0, 10)
    assert isinstance(triangular_function, TrapezoidFunction)
    triangular_function = TriangularFunction(0, 0.1, 1)
    assert isinstance(triangular_function, TrapezoidFunction)
    triangular_function = TriangularFunction(-2, -1, -0.2)
    assert isinstance(triangular_function, TrapezoidFunction)


def test_triangular_constructor_wrong_values() -> None:
    # Sanity checks
    pytest.raises(AssertionError, TriangularFunction, 0, -1, 2)
    pytest.raises(AssertionError, TriangularFunction, 0, 1, 0)
    pytest.raises(AssertionError, TriangularFunction, 0, 0, 0)
    pytest.raises(AssertionError, TriangularFunction, -1, -1, 2)
    pytest.raises(AssertionError, TriangularFunction, 0, 1, 1)
