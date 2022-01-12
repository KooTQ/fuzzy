"""
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
from fuzzy.functions import (
    TrapezoidFunction, InfiniteTrapezoidFunction, TriangularFunction
)


def test_triangular_function_call_correct_values(
        left: float = 0.2,
        top: float = 0.5,
        right: float = 0.8
) -> None:
    funct = TriangularFunction(left, top, right)
    args = [left - 1, left,
            (left + top) / 2,
            top,
            (right + top) / 2,
            right, right + 1]
    outputs = [0, 0, 1/2, 1., 1/2, 0, 0]
    assert_almost_equal_for_single_argument_function(funct, args, outputs)

    calc_args = [-1000000, -100, -50, -10, -2, -0.25, 0., 0.5, 1., 10., 20.,
                 1000]
    calc_outs = []
    for c_arg in calc_args:
        if c_arg < left:
            out = 0.
        elif c_arg < top:
            out = (c_arg - left)/(top - left)
        elif c_arg < right:
            out = (right - c_arg)/(right - top)
        else:
            out = 0.
        calc_outs.append(out)
    assert_almost_equal_for_single_argument_function(funct, calc_args,
                                                     calc_outs)


def test_multiple_triangular_function_call_correct_values() -> None:
    test_triangular_function_call_correct_values(-1., 0, 1)
    test_triangular_function_call_correct_values(-100., 0, 100)
    test_triangular_function_call_correct_values(-0.1, 0, 0.1)
    test_triangular_function_call_correct_values(-1., -0.95, 1)
    test_triangular_function_call_correct_values(-1., -0.95, 100)
    test_triangular_function_call_correct_values(-1., 0.95, 1)
    test_triangular_function_call_correct_values(-1.00, 0.95, 1)
    test_triangular_function_call_correct_values(-1000., -999., -998)
    test_triangular_function_call_correct_values(998., 999., 1000.)


def test_trapezoid_function_call_correct_values(
        lower_boundary: float = 0.2,
        min_full_boundary: float = 0.4,
        max_full_boundary: float = 0.6,
        upper_boundary: float = 0.8
) -> None:
    funct = TrapezoidFunction(
        lower_boundary=lower_boundary,
        min_full_boundary=min_full_boundary,
        max_full_boundary=max_full_boundary,
        upper_boundary=upper_boundary
    )
    funct_args = [lower_boundary - 1, lower_boundary,
                  (lower_boundary + min_full_boundary) / 2,
                  min_full_boundary,
                  (min_full_boundary + max_full_boundary) / 2,
                  max_full_boundary,
                  (max_full_boundary + upper_boundary) / 2,
                  upper_boundary, upper_boundary + 1]
    outputs = [0., 0., 0.5, 1, 1, 1, 0.5, 0, 0]
    assert_almost_equal_for_single_argument_function(funct, funct_args, outputs)

    calc_args = [-1000000, -100, -50, -10, -2, -0.25, 0., 0.5, 1., 10., 20.,
                 1000]
    calc_outs = []
    for c_arg in calc_args:
        if c_arg < lower_boundary:
            out = 0.
        elif c_arg < min_full_boundary:
            out = (c_arg - lower_boundary)/(min_full_boundary - lower_boundary)
        elif c_arg < max_full_boundary:
            out = 1.
        elif c_arg < upper_boundary:
            out = (upper_boundary - c_arg)/(upper_boundary - max_full_boundary)
        else:
            out = 0.
        calc_outs.append(out)
    assert_almost_equal_for_single_argument_function(
        funct, calc_args, calc_outs
    )


def assert_almost_equal_for_single_argument_function(
        funct,
        funct_args,
        expected_outputs
) -> None:
    for arg, out in zip(funct_args, expected_outputs):
        res = funct(arg)
        assert round(res-out, 5) == 0


def test_multiple_good_trapezoid_function_calls() -> None:
    test_trapezoid_function_call_correct_values(0, 1, 2, 3)
    test_trapezoid_function_call_correct_values(-100, -20, 0, 3)
    test_trapezoid_function_call_correct_values(-100, -21, 2, 400)
    test_trapezoid_function_call_correct_values(0, 0.1, 200, 200.1)
    test_trapezoid_function_call_correct_values(-0.1, 0, 0.1, 1)


def test_infinite_trapezoid_call_correct_values(
        left_vertex: float = 0.5,
        right_vertex: float = 0.75,
        side: str = 'left'
) -> None:
    funct = InfiniteTrapezoidFunction(
        left_vertex=left_vertex,
        right_vertex=right_vertex,
        infinite_side=side
    )
    args = [left_vertex - 1, left_vertex,
            (left_vertex + right_vertex) / 2,
            right_vertex, right_vertex + 1]
    if side == 'left':
        outputs = [1, 1, 1/2, 0, 0]
    else:
        outputs = [0, 0, 1/2, 1, 1]
    assert_almost_equal_for_single_argument_function(funct, args, outputs)

    calc_args = [-1000000, -100, -50, -10, -2, -0.25, 0., 0.5, 1., 10., 20.,
                 1000]
    calc_outs = []
    for c_arg in calc_args:
        if side == 'left':
            if c_arg < left_vertex:
                out = 1.
            elif c_arg < right_vertex:
                out = (right_vertex - c_arg)/(right_vertex - left_vertex)
            else:
                out = 0.
        else:  # side == 'right'
            if c_arg < left_vertex:
                out = 0.
            elif c_arg < right_vertex:
                out = (c_arg - left_vertex)/(right_vertex - left_vertex)
            else:
                out = 1.

        calc_outs.append(out)
    assert_almost_equal_for_single_argument_function(funct, calc_args,
                                                     calc_outs)


def test_multiple_infinite_trapezoids_call_correct_values() -> None:
    test_infinite_trapezoid_call_correct_values(0, 1, 'left')
    test_infinite_trapezoid_call_correct_values(0, 0.1, 'left')
    test_infinite_trapezoid_call_correct_values(-1, 0, 'left')
    test_infinite_trapezoid_call_correct_values(-1, 0.9, 'left')
    test_infinite_trapezoid_call_correct_values(-1, 1, 'left')
    test_infinite_trapezoid_call_correct_values(-1000, -100, 'left')
    test_infinite_trapezoid_call_correct_values(-1000, 1, 'left')
    test_infinite_trapezoid_call_correct_values(0, 100, 'left')
    test_infinite_trapezoid_call_correct_values(0, 1000, 'left')
    test_infinite_trapezoid_call_correct_values(0, 1, 'right')
    test_infinite_trapezoid_call_correct_values(0, 0.1, 'right')
    test_infinite_trapezoid_call_correct_values(-1, 0, 'right')
    test_infinite_trapezoid_call_correct_values(-1, 0.9, 'right')
    test_infinite_trapezoid_call_correct_values(-1, 1, 'right')
    test_infinite_trapezoid_call_correct_values(-1000, -100, 'right')
    test_infinite_trapezoid_call_correct_values(-1000, 1, 'right')
    test_infinite_trapezoid_call_correct_values(0, 100, 'right')
    test_infinite_trapezoid_call_correct_values(0, 1000, 'right')
