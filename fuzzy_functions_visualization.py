"""
Use of matplotlib library to visualize single and codependent fuzzy functions.
"""
import numpy as np
import matplotlib.pyplot as plt

from functions import TrapezoidFunction
from operators import TNorm, SNorm, StrongNegation


def visualize_fuzzy_trapezoid_functions(
        fuzz_funct: TrapezoidFunction
) -> None:
    """
    Visualize given trapezoid fuzzy membership function.

    :param fuzz_funct: trapezoid fuzzy membership function for visualization
    """
    figure = plt.figure()
    axes1 = figure.add_axes([0.1, 0.1, 0.9, 0.9])
    input_space_flat = np.linspace(-0.5, fuzz_funct.lower_boundary)
    input_space_asc = np.linspace(
        fuzz_funct.lower_boundary,
        fuzz_funct.min_full_boundary
    )
    input_space_high_plateau = np.linspace(
        fuzz_funct.min_full_boundary,
        fuzz_funct.max_full_boundary
    )
    input_space_desc = np.linspace(
        fuzz_funct.max_full_boundary,
        fuzz_funct.upper_boundary
    )
    input_space_end_flat = np.linspace(
        fuzz_funct.upper_boundary,
        1.5
    )
    output_space_flat = np.array(
        [fuzz_funct(in_point) for in_point in input_space_flat]
    )
    output_space_asc = np.array(
        [fuzz_funct(in_point) for in_point in input_space_asc]
    )
    output_space_plateau = np.array(
        [fuzz_funct(in_point) for in_point in input_space_high_plateau]
    )
    output_space_desc = np.array(
        [fuzz_funct(in_point) for in_point in input_space_desc]
    )
    output_space_end_flat = np.array(
        [fuzz_funct(in_point) for in_point in input_space_end_flat]
    )
    input_space = np.concatenate(
        [input_space_flat,
         input_space_asc,
         input_space_high_plateau,
         input_space_desc,
         input_space_end_flat])
    output_space = np.concatenate(
        [output_space_flat,
         output_space_asc,
         output_space_plateau,
         output_space_desc,
         output_space_end_flat])
    axes1.plot(input_space, output_space)
    axes1.scatter([
        fuzz_funct.lower_boundary,
        fuzz_funct.min_full_boundary,
        fuzz_funct.max_full_boundary,
        fuzz_funct.upper_boundary
    ], [
        fuzz_funct(fuzz_funct.lower_boundary),
        fuzz_funct(fuzz_funct.min_full_boundary),
        fuzz_funct(fuzz_funct.max_full_boundary),
        fuzz_funct(fuzz_funct.upper_boundary)
    ], color='navy')
    figure.show()


def visualize_fuzzy_operators(
        fuzz_funct1: TrapezoidFunction,
        fuzz_funct2: TrapezoidFunction,
        fuzz_funct3: TrapezoidFunction
) -> None:
    """
    Visualize given trapezoid fuzzy operators.

    Equation is of operators that will be applied and visualized:
      equation = (fuzz_funct1 AND (NOT fuzz_funct2)) OR fuzz_funct3

    :param fuzz_funct1: trapezoid fuzzy membership function for visualization
    :param fuzz_funct2: trapezoid fuzzy membership function for visualization
    :param fuzz_funct3: trapezoid fuzzy membership function for visualization
    """
    figure = plt.figure()
    axes1 = figure.add_axes([0.1, 0.1, 0.9, 0.9])
    fuzz_funct = SNorm(TNorm(fuzz_funct1, StrongNegation(fuzz_funct2)),
                       fuzz_funct3)
    input_space = np.linspace(-1, 2.5, num=500)

    output_space = np.array(
        [fuzz_funct(in_point) for in_point in input_space]
    )
    axes1.plot(input_space, output_space)
    figure.show()

if __name__ == '__main__':
    _function = TrapezoidFunction(-0.25, 0.5, 0.75, 1.1)
    visualize_fuzzy_trapezoid_functions(_function)

    _function1 = TrapezoidFunction(-0.25, 0.0, 0.75, 1.1)
    _function2 = TrapezoidFunction(-0.25, 0.5, 0.75, 1.1)
    _function3 = TrapezoidFunction(-0.1, 0.1, 0.2, 0.3)
    visualize_fuzzy_trapezoid_functions(_function1)
    visualize_fuzzy_trapezoid_functions(_function2)
    visualize_fuzzy_trapezoid_functions(_function3)
    visualize_fuzzy_operators(_function1, _function2, _function3)
