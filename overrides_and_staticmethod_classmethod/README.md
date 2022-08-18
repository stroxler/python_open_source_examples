# Does the order of @override WRT @classmethod / @staticmethod matter?

If the @override decorator is a pure no-op at runtime then the answer
will be no trivially.

But if we have any runtime behavior, I believe the answer is yes, the
descriptor magic of `@classmethod` and `@staticmethod` need to run last
in order to get the correct behavior.

Here is a small demo illustrating that even if we choose not to have runtime
enforcement of overrides, even a very minimal runtime behavior like
setting the `__override__` attribute would fail if the ordering were
incorrect:
```
> python demo.py
Below.normal_method: True
Below().normal_method: True
Below.class_method: True
Below.static_method: True
Above.normal_method: True
Above().normal_method: True
Above.class_method has no __override__ attribute
Above.static_method has no __override__ attribute
```
