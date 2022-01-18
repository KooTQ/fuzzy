"""
Tests for operations on fuzzy membership degree options.

Sanity checks:
  - Any operation must return values within range `[0., 1.]`
  - Any operation take as an argument any value from range
    `[float('-inf'), float('inf')]`
  - Operations can be stacked and combine in any order
  - Operations can be stacked many times
  - not t-norm nor s-norm can be higher than both of functions
  - not t-norm nor s-norm can be lower than both of functions
  - t-norm or s-norm applied on 2 instances of same function `f`
    must result with same results as function `f`

Negation:
  - For any function - double negation must return same
    results as given function

Operators should be tested on:
  - Triangular membership functions
  - Trapezoid membership functions
  - Infinite trapezoid MF
  - combination of any and all of the above
"""
import random
import numpy as np

from fuzzy.operators import StrongNegation, TNorm, SNorm
from fuzzy.functions import (
    TriangularFunction, InfiniteTrapezoidFunction, TrapezoidFunction
)


def test_double_strong_negation_on_triangular_membership_functions() -> None:
    trial_funct = TriangularFunction(0, 1, 2)
    values = np.linspace(-2, 3, 50)
    degrees_of_memb = np.array([trial_funct(v) for v in values])
    neg_neg_funct = StrongNegation(StrongNegation(trial_funct))
    degrees_of_memb_neg = np.array([neg_neg_funct(v) for v in values])
    assert -1e-5 < np.sum(degrees_of_memb - degrees_of_memb_neg) < 1e-5


def test_double_strong_negation_on_triangular_membership_function_n_times(
        n: int = 5
) -> None:
    for _ in range(n):
        base = random.randint(-100, 100)
        left = base + (random.random()**2) * 100
        top = left + (random.random()**2) * 100
        right = top + (random.random()**2) * 100
        trial_funct = TriangularFunction(left, top, right)

        values = np.linspace(base - 10, right + 10, 50)
        degrees_of_memb = np.array([trial_funct(v) for v in values])
        neg_neg_funct = StrongNegation(StrongNegation(trial_funct))
        degrees_of_memb_neg = np.array([neg_neg_funct(v) for v in values])
        assert -1e-5 < np.sum(degrees_of_memb - degrees_of_memb_neg) < 1e-5


def test_10_tier_rule_operation_on_infinite_trapezoid_functions() -> None:
    funct1 = InfiniteTrapezoidFunction(0.2, 0.5, 'left')
    funct2 = InfiniteTrapezoidFunction(-0.2, 20, 'left')
    funct3 = InfiniteTrapezoidFunction(20, 20.1, 'right')
    op1 = StrongNegation(funct1)
    op2 = TNorm(op1, funct1)
    op3 = SNorm(op2, funct2)
    op4 = TNorm(funct3, funct1)
    op5 = StrongNegation(op4)
    op6 = TNorm(op4, op5)
    op7 = StrongNegation(funct3)
    op8 = TNorm(op6, op7, funct1)
    op9 = TNorm(op3, funct3)
    op10 = SNorm(op8, op9, op4)
    values = np.linspace(-1, 21, 200)
    for v in values:
        res = op10(v)
        assert 0. <= res <=1


def test_t_norm_not_higher_nor_lower_than_inner_trapezoid_functions() -> None:
    funct1 = _create_random_trapezoid_function()
    funct2 = _create_random_trapezoid_function()
    funct3 = _create_random_trapezoid_function()
    op1 = TNorm(funct1, funct2)
    op2 = TNorm(funct1, funct2, funct3)
    values1 = np.linspace(funct1.lower_boundary - 1,
                          funct1.upper_boundary, 50)
    values2 = np.linspace(funct2.lower_boundary - 1,
                          funct2.upper_boundary, 50)
    values3 = np.linspace(funct3.lower_boundary - 1,
                          funct3.upper_boundary, 50)
    _assert_higher_lower(values1, funct1, funct2, funct3, op1, op2)
    _assert_higher_lower(values2, funct1, funct2, funct3, op1, op2)
    _assert_higher_lower(values3, funct1, funct2, funct3, op1, op2)


def test_s_norm_not_higher_nor_lower_than_inner_trapezoid_functions() -> None:
    funct1 = _create_random_trapezoid_function()
    funct2 = _create_random_trapezoid_function()
    funct3 = _create_random_trapezoid_function()
    op1 = SNorm(funct1, funct2)
    op2 = SNorm(funct1, funct2, funct3)
    values1 = np.linspace(funct1.lower_boundary - 1,
                          funct1.upper_boundary, 50)
    values2 = np.linspace(funct2.lower_boundary - 1,
                          funct2.upper_boundary, 50)
    values3 = np.linspace(funct3.lower_boundary - 1,
                          funct3.upper_boundary, 50)
    _assert_higher_lower(values1, funct1, funct2, funct3, op1, op2)
    _assert_higher_lower(values2, funct1, funct2, funct3, op1, op2)
    _assert_higher_lower(values3, funct1, funct2, funct3, op1, op2)


def _assert_higher_lower(values, f1, f2, f3, op1, op2) -> None:
    for v in values:
        res1 = f1(v)
        res2 = f2(v)
        res3 = f3(v)
        op1_res = op1(v)
        op2_res = op2(v)
        assert op1_res <= max([res1, res2, res3])
        assert op2_res <= max([res1, res2, res3])
        assert op1_res >= min([res1, res2, res3])
        assert op2_res >= min([res1, res2, res3])




def test_t_norm_in_range_0_to_1() -> None:
    funct1 = _create_random_trapezoid_function()
    funct2 = _create_random_trapezoid_function()
    funct3 = _create_random_trapezoid_function()
    op1 = TNorm(funct1, funct2)
    op2 = TNorm(funct1, funct2, funct3)
    values1 = np.linspace(funct1.lower_boundary - 1,
                          funct1.upper_boundary, 50)
    values2 = np.linspace(funct2.lower_boundary - 1,
                          funct2.upper_boundary, 50)
    values3 = np.linspace(funct3.lower_boundary - 1,
                          funct3.upper_boundary, 50)
    _assert_higher_lower(values1, funct1, funct2, funct3, op1, op2)
    _assert_higher_lower(values2, funct1, funct2, funct3, op1, op2)
    _assert_higher_lower(values3, funct1, funct2, funct3, op1, op2)


def test_s_norm_in_range_0_to_1() -> None:
    funct1 = _create_random_trapezoid_function()
    funct2 = _create_random_trapezoid_function()
    funct3 = _create_random_trapezoid_function()
    op1 = SNorm(funct1, funct2)
    op2 = SNorm(funct1, funct2, funct3)
    values1 = np.linspace(funct1.lower_boundary - 1,
                          funct1.upper_boundary, 50)
    values2 = np.linspace(funct2.lower_boundary - 1,
                          funct2.upper_boundary, 50)
    values3 = np.linspace(funct3.lower_boundary - 1,
                          funct3.upper_boundary, 50)
    _assert_0_to_1(values1, op1, op2)
    _assert_0_to_1(values2, op1, op2)
    _assert_0_to_1(values3, op1, op2)


def _assert_0_to_1(values, op1, op2) -> None:
    for v in values:
        op1_res = op1(v)
        op2_res = op2(v)
        assert op1_res <= 1.0
        assert op2_res <= 1.0
        assert op1_res >= 0.0
        assert op2_res >= 0.0


def _create_random_trapezoid_function() -> TrapezoidFunction:
    base = random.randint(-100, 100)
    left = base + (random.random() ** 2) * 100
    top_l = left + (random.random() ** 2) * 100
    top_r = top_l + (random.random() ** 2) * 100
    right = top_r + (random.random() ** 2) * 100
    return TrapezoidFunction(left, top_l, top_r, right)


def _create_random_triangular_function() -> TriangularFunction:
    base = random.randint(-100, 100)
    left = base + (random.random() ** 2) * 100
    top = left + (random.random() ** 2) * 100
    right = top + (random.random() ** 2) * 100
    return TriangularFunction(left, top, right)
