"""
Fuzzy Rules are objects containing Operation pointing towards fuzzy function.

Rules are IF-THEN statements that are constructed of FuzzyFunctions and
FuzzyOperators. Rule can be written down in plain english.

For example Rule could be:
  - IF low temperature AND not high pressure THEN high fan throttle.

"""
from fuzzy.rules._rules import FuzzyRule
