# How does Python resolve imports

If I'm in a location `package/some_module.py`
and I run `from . import subpackage0`, it will generally
(a) first import `package/__init__.py`
(b) then check whether the name `subpackage0` is bound there
(c) if not, import `package/subpackage0.py`

But it does work to use `from . import subpackage0` *in* the
`__init__.py` module. I'm not certain how this works, my guess
is that Python knows that it's in the process of importing
`__init__.py` already and so it knows to jump straight to the
subpackage.
