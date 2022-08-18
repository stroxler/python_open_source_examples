def override(f):
    setattr(f, "__override__", True)
    return f



class Base:
    def normal_method(self) -> None:
        pass

    @property
    def prop(self) -> int:
        return 42

    @classmethod
    def class_method(cls) -> None:
        pass

    @staticmethod
    def static_method() -> None:
        pass



class Below(Base):

    @override
    def normal_method(self) -> None:
        pass

    @property
    @override
    def prop(self) -> int:
        return 42


    @classmethod
    @override
    def class_method(cls) -> None:
        pass

    @staticmethod
    @override
    def static_method() -> None:
        pass


print("--- @override below special decorators ---")
print(f"Below.normal_method: {getattr(Below.normal_method, '__override__')}")
try:
    print(f"Below.prop: {getattr(Below.prop, '__override__')}")
except AttributeError as e:
    print(f"Below.prop: {e}")
try:
    print(f"Below.prop.fget: {getattr(Below.prop.fget, '__override__')}")
except AttributeError as e:
    print(f"Below.prop: {e}")
print(f"Below().normal_method: {getattr(Below().normal_method, '__override__')}")
print(f"Below.class_method: {getattr(Below.class_method, '__override__')}")
print(f"Below.static_method: {getattr(Below.static_method, '__override__')}")


prop_message = None

class Above(Base):
    @override
    def normal_method(self) -> None:
        pass

    try:
        @override
        @property
        def prop(self) -> int:
            return 42
    except AttributeError:
        global prop_message
        prop_message = "Above.prop: Could not even set __override__ on property descriptor!"

    @override
    @classmethod
    def class_method(cls) -> None:
        pass

    @override
    @staticmethod
    def static_method() -> None:
        pass



print("--- @override above special decorators ---")
print(f"Above.normal_method: {getattr(Above.normal_method, '__override__')}")
print(f"Above().normal_method: {getattr(Above().normal_method, '__override__')}")
if prop_message is not None:
    print(prop_message)
else:
    # this code doesn't wind up being run
    try:
        print(f"Above.prop: {getattr(Above.prop, '__override__')}")
    except AttributeError as e:
        print(f"Above.prop: {e}")
try:
    print(f"Above.class_method: {getattr(Above.class_method, '__override__')}")
except AttributeError as e:
    print(f"Above.class_method: {e}")
try:
    print(f"Above.static_method: {getattr(Above.static_method, '__override__')}")
except AttributeError as e:
    print(f"Above.static_method: {e}")
