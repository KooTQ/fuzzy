from fuzzy.functions import FuzzyMembershipFunction, TrapezoidFunction

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