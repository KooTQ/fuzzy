import pytest

from fuzzy.functions import TrapezoidFunction

"""
    lower_boundary: float
    min_full_boundary: float
    max_full_boundary: float
    upper_boundary: float
Unit tests TrapezoidFunction.__init__:
  1. set in constructor *lower_boundary* with higher than *upper_boundary*
  1. set in constructor *min_full_boundary* with higher than *upper_boundary*
  1. set in constructor *max_full_boundary* with higher than *upper_boundary*
  1. set in constructor *lower_boundary* with higher than *max_full_boundary*
  1. set in constructor *min_full_boundary* with higher than *max_full_boundary* 
  1. set in constructor *lower_boundary* with higher than *min_full_boundary* 

Unit tests TrapezoidFunction.__call__:
  1. None as argument.
  1. ``float('-inf')`` as argument
  1. ``float('inf')`` as argument
  1. ``0.`` as argument
  1. ``1.`` as argument

  1. To ``TrapezoidFunction(0, 1, 2, 3)`` argument ``0.`` assert ``0.``
  1. To ``TrapezoidFunction(0, 1, 2, 3)`` argument ``1.`` assert ``1.``
  1. To ``TrapezoidFunction(0, 1, 2, 3)`` argument ``2.`` assert ``1.``
  1. To ``TrapezoidFunction(0, 1, 2, 3)`` argument ``3.`` assert ``0.``

  1. To ``TrapezoidFunction(0, 1, 2, 3)`` argument ``0.5`` assert ``0.5``
  etc.
"""


def test_typical_trapezoid_membership_objects():
    # Typical trapezoid membership functions - with start, end, ascending slope,
    #  plateau and descending slope. ___/‾\_ or _/‾\___ or _/‾‾‾‾\_ or similar.
    t1 = TrapezoidFunction(0., 1., 2., 3.)
    assert isinstance(t1, TrapezoidFunction)
    t1 = TrapezoidFunction(-1., 0.1, 0.11, 5.)
    assert isinstance(t1, TrapezoidFunction)


def test_infinite_trapezoid_membership_function_objects():
    t0 = TrapezoidFunction(float('-inf'), 0., 1., float('inf'))
    assert isinstance(t0, TrapezoidFunction)


def test_wrong_infinite_trapezoid_membership_function_objects():
    # Infinity should be either on both vertices of ascending slope
    #  or on both vertices of descending slope.
    pytest.raises(AssertionError, TrapezoidFunction,
                  float('-inf'), 0., 1., 2)
    pytest.raises(AssertionError, TrapezoidFunction,
                  -1, 0., 1., float('inf'))

    # There can be only one
    pytest.raises(AssertionError, TrapezoidFunction,
                  float('-inf'), 0., 1., float('inf'))
    pytest.raises(AssertionError, TrapezoidFunction,
                  float('-inf'), 0., 1., float('inf'))


def test_wrong_vertices_values():
    pytest.raises(AssertionError, TrapezoidFunction, 0., -1., 2., 3.)
    pytest.raises(AssertionError, TrapezoidFunction, 0., 1., -1., 3.)
    pytest.raises(AssertionError, TrapezoidFunction, 0., 1., 2., -1.)

    pytest.raises(AssertionError, TrapezoidFunction, 0., 1., 0.5, 3.)
    pytest.raises(AssertionError, TrapezoidFunction, 0., 1., 2., 0.5)

    pytest.raises(AssertionError, TrapezoidFunction, 0., 1., 2., 1.5)
    pytest.raises(AssertionError, TrapezoidFunction, 0., 1., 2., -1.)

    pytest.raises(AssertionError, TrapezoidFunction, 0., 0., 0., 0.)
