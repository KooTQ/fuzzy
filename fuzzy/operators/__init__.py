"""
This package contains operators for fuzzy membership functions.

Fuzzy sets are represented as fuzzy membership functions used to
  evaluate degree of membership for given element in fuzzy set.
  As classical sets have operators like union, negation and intersection -
  fuzzy sets have respectively fuzzy s-norm, fuzzy strong negation
  and fuzzy intersection.

For complex scenarios' membership functions can be joined with operators
  into more complex systems. For example, if we want to regulate temperature
  in the laundry room, we could use this toy system:
  \"If humidity in room is high *AND* room is *NOT* uncomfortably hot - increase
  temperature slightly.\" - *AND* and *NOT* are respectively fuzzy t-norm and
  fuzzy strong negation.

"""
from fuzzy.operators._operators import (
    FuzzyOperator, TNorm, SNorm, StrongNegation, Operatable
)
