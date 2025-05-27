import pickle
import os
import json
from dataclasses import dataclass, field, asdict
from typing import Optional, Protocol, TypeVar, Sequence, Generic, runtime_checkable


@dataclass(order=True)
class User:
    sort_index: str = field(init=False, repr=False)
    id: int  # noqa: A003
    name: str
    login: str
    password: str = field(repr=False)
    email: Optional[str] = None
    address: Optional[str] = None

    def __post_init__(self):
        self.sort_index = self.name

    def to_dict(self) -> dict:
        data = asdict(self)
        data.pop("password", None)
        return data


T = TypeVar('T')


@runtime_checkable
class IDataRepository(Protocol[T]):
    def get_all(self) -> Sequence[T]:
        pass

    def get_by_id(self, id: int) -> Optional[T]:
        pass

    def add(self, item: T) -> None:
        pass

    def update(self, item: T) -> None:
        pass

    def delete(self, item: T) -> None:
        pass


class IUserRepository(IDataRepository[User], Protocol):
    def get_by_login(self, login: str) -> Optional[User]:
        pass


class DataRepository(Generic[T], IDataRepository[T]):
    def __init__(self, filepath: str):
        self.filepath = filepath
        self._data: list[T] = self._load()

    def _load(self) -> list[T]:
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'rb') as f:
                    return pickle.load(f)
            except (OSError, pickle.PickleError) as e:
                print(f"Ошибка при загрузке данных из {self.filepath}: {e}")
        return []

    def _save(self) -> None:
        try:
            with open(self.filepath, 'wb') as f:
                pickle.dump(self._data, f)
        except (OSError, pickle.PickleError) as e:
            print(f"Ошибка при сохранении данных в {self.filepath}: {e}")

    def get_all(self) -> Sequence[T]:
        return list(self._data)

    def get_by_id(self, id: int) -> Optional[T]:
        return next((item for item in self._data if getattr(item, 'id', None) == id), None)

    def add(self, item: T) -> None:
        self._data.append(item)
        self._save()

    def update(self, item: T) -> None:
        for i, existing in enumerate(self._data):
            if getattr(existing, 'id', None) == getattr(item, 'id', None):
                self._data[i] = item
                self._save()
                return

    def delete(self, item: T) -> None:
        self._data = [x for x in self._data if getattr(x, 'id', None) != getattr(item, 'id', None)]
        self._save()


class UserRepository(IUserRepository):
    def __init__(self, filepath: str):
        self.repo = DataRepository[User](filepath)

    def get_all(self) -> Sequence[User]:
        return self.repo.get_all()

    def get_by_id(self, id: int) -> Optional[User]:
        return self.repo.get_by_id(id)

    def add(self, item: User) -> None:
        self.repo.add(item)

    def update(self, item: User) -> None:
        self.repo.update(item)

    def delete(self, item: User) -> None:
        self.repo.delete(item)

    def get_by_login(self, login: str) -> Optional[User]:
        return next((u for u in self.repo.get_all() if u.login == login), None)


class IAuthService(Protocol):
    def sign_in(self, user: User) -> None:
        pass

    def sign_out(self) -> None:
        pass

    @property
    def is_authorized(self) -> bool:
        pass

    @property
    def current_user(self) -> Optional[User]:
        pass


class AuthService(IAuthService):
    def __init__(self, filepath: str, user_repo: IUserRepository) -> None:
        self.filepath = filepath
        self.user_repo = user_repo
        self._current_user: Optional[User] = self._load_user()

    def _load_user(self) -> Optional[User]:
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'rb') as f:
                    login = pickle.load(f)
                    return self.user_repo.get_by_login(login)
            except (OSError, pickle.PickleError) as e:
                print(f"Ошибка при загрузке пользователя из {self.filepath}: {e}")
        return None

    def _save_user(self) -> None:
        try:
            if self._current_user:
                with open(self.filepath, 'wb') as f:
                    pickle.dump(self._current_user.login, f)
            elif os.path.exists(self.filepath):
                os.remove(self.filepath)
        except (OSError, pickle.PickleError) as e:
            print(f"Ошибка при сохранении сессии пользователя: {e}")

    def sign_in(self, user: User) -> None:
        self._current_user = user
        self._save_user()

    def sign_out(self) -> None:
        self._current_user = None
        self._save_user()

    @property
    def is_authorized(self) -> bool:
        return self._current_user is not None

    @property
    def current_user(self) -> Optional[User]:
        return self._current_user


def print_json(message: str, data: dict | list | str) -> None:
    output = {
        "message": message,
        "data": data
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def demo():
    user_file = "users.json"
    auth_file = "auth.pkl"
    repo = UserRepository(user_file)
    auth = AuthService(auth_file, repo)

    print("=== Демонстрация ===")

    if not repo.get_by_login("alice123"):
        user = User(id=1, name="Alice", login="alice123", password="1234", email="alice@mail.com")
        repo.add(user)
        print("Добавлен пользователь:", user.name)
        print_json("Пользователь добавлен", user.to_dict())

    user = repo.get_by_login("alice123")
    if user and user.password == "1234":
        auth.sign_in(user)
        print("Авторизован как:", auth.current_user.name)
        print_json("Пользователь авторизован", user.to_dict())

    user.name = "Alice Smith"
    repo.update(user)
    print("Имя пользователя обновлено на:", user.name)
    print_json("Имя пользователя обновлено", user.to_dict())

    auth.sign_out()
    print("Выход из аккаунта.")
    print_json("Выход из аккаунта", "ok")

    auth = AuthService(auth_file, repo)
    if auth.is_authorized:
        print("Автоматически вошли как:", auth.current_user.name)
        print_json("Автоавторизация", auth.current_user.to_dict())
    else:
        print("Нет активной сессии.")
        print_json("Автоавторизация", "нет активной сессии")


if __name__ == "__main__":
    demo()
