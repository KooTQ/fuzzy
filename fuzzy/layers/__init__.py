"""
Layers are containers for fuzzy functions.

Each fuzzified domain can be granulated into N - usually 3, 5 or 7 -
fuzzy membership functions.

Granulation is amount of used fuzzy membership functions to cover given domain.

For example domain of temperature represented as Layer with granulation 3
could represent:
  - low temperature
  - moderate temperature
  - high temperature

Layers contain FuzzyRules for each contained fuzzy membership functions.
Layers contain cut-off mechanism.
Layers contain de-fuzzyfication mechanism.
Layers contain centroid finding mechanism.
"""
