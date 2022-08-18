# Does the order of @override WRT @classmethod / @staticmethod matter?

A question came up when drafting a PEP for an `@typing.override` of
whether the order of `@override` relative to `@staticmethod` and
`@classmethod` matters.

If the override decorator does nothing at all at run time, then the
answer would obviously be no. But we are also leaning toward having the
`@override` decorator set an `__override__` attribute so that runtime
introspection of the type information would be possible.


If we do this, then the order does matter. For example:

```python
class Base:
    @staticmethod
    def foo() -> None:
        pass

class OverrideBelow:
    # the __override__ attribute will be set correctly here
    @staticmethod
    @override
    def foo() -> None:
        pass

class OverrideAbove:
    # the __override__ attribute will be not be set here
    @override
    @staticmethod
    def foo() -> None:
        pass
```

What actually happens here is that

- In `OverrideBelow.foo`:
  - we set the `__override__` attribute on the raw function
  - the `@staticmethod` decorator wraps that raw funciton in
    a descriptor, where `__get__` returns the (appropriately
    bound) copy of the function. Since the function itself has
    `__override__` set, the output of the descriptor `__get__`
    will have it.
- In `OverrideAbove.foo`:
  - the `@statimethod` decorator wraps the raw function in a
    descriptor
  - the `@override` decorator then sets `__override__` on the
    descriptor itself, *not* on the function that will be returned
    by `__get__`. So normal code asking whether the `__override__`
    flag is set will see that it is not!
    
Other descriptors like `@property` and `@classmethod` will behave in
a simlilar way (although in the case of `@property` even trying to
set `__override__` on the descriptor produces a runtime error, I'm guessing
this is because property descriptors are C objects with fixed slots).


The takeaway is that these "special" decorators always need to come
*above* the @override decorator in order to get expected runtime
behavior.

# Demo of this behavior

In `demo.py` I test it out on all three of the standard, special descriptor
decorators:
```
> python demo.py

Below.normal_method: True
Below.prop: True
Below().normal_method: True
Below.class_method: True
Below.static_method: True

Above.normal_method: True
Above().normal_method: True
Above.prop: Could not even set __override__ on property descriptor!
Above.class_method has no __override__ attribute
Above.static_method has no __override__ attribute
```

