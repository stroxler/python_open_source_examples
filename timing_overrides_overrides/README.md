# Timing `overrides.overrides`

This is to inform a decision about whether a new `typing.override`
decorator should include runtime enforcement; since we have a ready-made
runtime-enforced decorator in `overrides.overrides` we can compare that
to a minimal implementation that does nothing beyond set the `__override__`
dunder attribute.

Setup:
```bash
pyenv install 3.10.6
pyenv local 3.10.6
pyenv virtualenv time_overrides
pyenv local time_overrides
pip install overrides==6.2.0
```

Test:
```
> time python with_pass_through.py
finished!

real	0m0.219s
user	0m0.131s
sys	0m0.059s

> time python3 with_overrides.py
Finished!

real	0m6.442s
user	0m6.277s
sys	0m0.089s
```

This suggests that the current implementation of overrides has
something like (6s / 50K) = 120 microseconds of overhead.

# Optimizations?

I am not much of a metaprogramming expert; the `overrides` implementation
is [here](https://github.com/mkorpela/overrides/blob/main/overrides/overrides.py)
and it may well be possible to speed this up by a significant factor.
