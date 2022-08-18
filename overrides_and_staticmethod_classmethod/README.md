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
    
The `@classmethod` decorator behaves similarly.

The `@property` decorator is a bit more involved, in both cases:
- trying to put the `@override` decorator above the `@property`
  decorator will *immediately* throw a runtime error. I think this
  is because the descriptor that it produces has a low-level
  implementation with fixed slots, so the setattr call fails.
- trying to put the `@override` decorator above the `@property`
  decorator is okay at runtime, but it's still not possible to
  trivially introspect.
  - The underlying problem is that the property descriptor isn't implemented in
    terms of just a `__get__`, it actually has separate hooks for get and set.
    - This makes sense: at runtime it would be entirely possible for only one
      of the getter or setter to be overridden, so there needs to be a way to
      ask about each one separately
  - You *can* still introspect at runtime, you simply have to look up
    the `fget` and `fset` fields on the property when doing introspection.


The takeaways are that:
- in all cases, the special decorators need to be evaluated last
  (so `@override` should go *below* them)
- in the case of `@property` any runtime use of `__override__` must
  moreover be sure to distinguish `fget` vs `fset`.

# Demo of this behavior

In `demo.py` I test it out on all three of the standard, special descriptor
decorators:
```
> python demo.py
--- @override below special decorators ---
Below.normal_method: True
Below.prop: 'property' object has no attribute '__override__'
Below.prop.fget: True
Below().normal_method: True
Below.class_method: True
Below.static_method: True
--- @override above special decorators ---
Above.normal_method: True
Above().normal_method: True
Above.prop: Could not even set __override__ on property descriptor!
Above.class_method: 'function' object has no attribute '__override__'
Above.static_method: 'function' object has no attribute '__override__'
```


