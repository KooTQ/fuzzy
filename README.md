Fuzzy reasoning systems are systems of fuzzy logic.
Classical logic and reasoning systems are using only values of ``True``
   or ``False`` and operators taking logical values and returning logical value.
However fuzzy reasoning system are relative. Value of fuzzy statment can be
   *barely*, *somewhat*, and even *strongly* ``True`` or anything in between.

Imagine classical set. Some object can be *contained* in set or
   can be *not contained* in set. Fuzzy set can use *membership function* to
   determine degree of membership for any object.
   
Simplest way to show importance of fuzzy logic is using common use temperature.
   Most people don't use feeling cold as definitive statement. People would usualy
   distinguish: *"It is quite cold outside."*, *"It is a little cold outside"*, 
   and *"It is very cold outside."* rather than for all *cold scenarios*,
   use definitive *"Temperature falls in cold category."*. 

If we arbitrarily assume *cold temperature set* is 
   set of temperature values ```t < 20°C```, we will lose distinction 
   between ``t = 20°C``, ``t = 10°C``, and ``t = 0°C``.
   Also in this scenario close values like ``t0 = 19.93°C``, and ``t1 = 20.03°C`` 
   would be treated as less similar than ``t0 = 19.93°C`` and ``t2 = -30°C``.

Not only input values can be fuzzified - controlling output measure can be too. 
   After hearing *"It is very cold here"* reasonable action is to 
   *"Increase heating strongly."*, but after hearing 
   *"It is a little cold in here"* to *"Increase heating slightly."*.
