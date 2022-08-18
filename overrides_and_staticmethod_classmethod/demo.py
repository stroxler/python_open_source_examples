def override(f):
    setattr(f, "__override__", True)
    return f



class Base:
    def normal_method(self) -> None:
        pass

    @classmethod
    def class_method(cls) -> None:
        pass

    @staticmethod
    def static_method() -> None:
        pass


class Above(Base):
    @override
    def normal_method(self) -> None:
        pass

    @override
    @classmethod
    def class_method(cls) -> None:
        pass

    @override
    @staticmethod
    def static_method() -> None:
        pass


class Below(Base):
    @override
    def normal_method(self) -> None:
        pass

    @classmethod
    @override
    def class_method(cls) -> None:
        pass

    @staticmethod
    @override
    def static_method() -> None:
        pass


print(f"Below.normal_method: {getattr(Below.normal_method, '__override__')}")
print(f"Below().normal_method: {getattr(Below().normal_method, '__override__')}")
print(f"Below.class_method: {getattr(Below.class_method, '__override__')}")
print(f"Below.static_method: {getattr(Below.static_method, '__override__')}")

print(f"Above.normal_method: {getattr(Above.normal_method, '__override__')}")
print(f"Above().normal_method: {getattr(Above().normal_method, '__override__')}")
try:
    print(f"Above.class_method: {getattr(Above.class_method, '__override__')}")
except AttributeError:
    print("Above.class_method has no __override__ attribute")
try:
    print(f"Above.static_method: {getattr(Above.static_method, '__override__')}")
except AttributeError:
    print("Above.static_method has no __override__ attribute")
