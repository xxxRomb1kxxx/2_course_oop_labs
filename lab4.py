from abc import ABC, abstractmethod
from typing import List, TypeVar, Any
T = TypeVar('T')


class PropertyChangedListenerProtocol(ABC):
    @abstractmethod
    def on_property_changed(self, obj: Any, property_name: str) -> None:
        pass


class PropertyChangingListenerProtocol(ABC):
    @abstractmethod
    def on_property_changing(self, obj: Any, property_name: str, old_value: T, new_value: T) -> bool:
        pass


class DataChangedProtocol(ABC):
    @abstractmethod
    def add_property_changed_listener(self, listener: PropertyChangedListenerProtocol) -> None:
        pass

    @abstractmethod
    def remove_property_changed_listener(self, listener: PropertyChangedListenerProtocol) -> None:
        pass


class DataChangingProtocol(ABC):
    @abstractmethod
    def add_property_changing_listener(self, listener: PropertyChangingListenerProtocol) -> None:
        pass

    @abstractmethod
    def remove_property_changing_listener(self, listener: PropertyChangingListenerProtocol) -> None:
        pass


class User(DataChangedProtocol, DataChangingProtocol):
    def __init__(self, name: str, age: int) -> None:
        self._name = name
        self._age = age
        self._changed_listeners: List[PropertyChangedListenerProtocol] = []
        self._changing_listeners: List[PropertyChangingListenerProtocol] = []

    def add_property_changed_listener(self, listener: PropertyChangedListenerProtocol) -> None:
        self._changed_listeners.append(listener)

    def remove_property_changed_listener(self, listener: PropertyChangedListenerProtocol) -> None:
        self._changed_listeners.remove(listener)

    def add_property_changing_listener(self, listener: PropertyChangingListenerProtocol) -> None:
        self._changing_listeners.append(listener)

    def remove_property_changing_listener(self, listener: PropertyChangingListenerProtocol) -> None:
        self._changing_listeners.remove(listener)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: Any) -> None:
        if self._changing_listeners:
            allowed = all(
                listener.on_property_changing(self, "name", self._name, value)
                for listener in self._changing_listeners
            )
            if not allowed:
                return

        self._name = value

        for listener in self._changed_listeners:
            listener.on_property_changed(self, "name")

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, value: Any) -> None:
        try:
            value = int(value)
        except (ValueError, TypeError):
            print("Validation failed: Age must be a number")
            return

        if self._age == value:
            return

        if self._changing_listeners:
            allowed: bool = all(
                listener.on_property_changing(self, "age", self._age, value)
                for listener in self._changing_listeners
            )
            if not allowed:
                return

        self._age = value

        for listener in self._changed_listeners:
            listener.on_property_changed(self, "age")


class LoggerListener(PropertyChangedListenerProtocol):
    def on_property_changed(self, obj: Any, property_name: str) -> None:
        print(f"[Logger] Property '{property_name}' changed in {obj.__class__.__name__}.\n"
              f" New value: {getattr(obj, property_name)}")


class AgeValidator(PropertyChangingListenerProtocol):
    def on_property_changing(self, obj: object, property_name: str, old_value: int, new_value: int) -> bool:
        if property_name == "age":
            if not isinstance(new_value, int) or new_value < 0:
                print("Validation failed: Age cannot be negative")
                return False
        return True


class NameValidator(PropertyChangingListenerProtocol):
    def on_property_changing(self, obj: object, property_name: str, old_value: str, new_value: str) -> bool:
        if property_name == "name":
            if len(new_value) < 2 or not new_value.isalpha():
                print("Validation failed: Name must be at least 2 letters")
                return False
        return True


if __name__ == "__main__":
    user = User("TRAVIS", 34)

    logger = LoggerListener()
    user.add_property_changed_listener(logger)

    age_validator = AgeValidator()
    name_validator = NameValidator()
    user.add_property_changing_listener(age_validator)
    user.add_property_changing_listener(name_validator)

    print("Valid changes:")
    user.name = "SCOTT"
    user.age = 52

    print("inValid changes:")
    user.name = "S"
    user.age = "-999999999999999999999"
    print("Finally")
    print(f"Name: {user.name}, Age: {user.age}")
