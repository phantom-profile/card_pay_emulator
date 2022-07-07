from typing import Protocol
from enum import Enum
from random import choice


class Genders(Enum):
    MALE = 'Мальчик'
    FEMALE = 'Девочка'
    STRANGE = 'Чудо-Юдо'


class Displayable(Protocol):
    def __str__(self) -> str: ...


class AnimalProtocol(Protocol):
    name: str
    age: int
    gender: Genders

    def gender_represent(self) -> str: ...


class Animal:
    def __init__(self, name: str):
        self.name = name
        self.age: int = 0
        self.gender: Genders = choice(list(Genders))

    def gender_represent(self) -> str:
        return self.gender.value.capitalize()

    def __str__(self) -> str:
        return f'Меня зовут {self.name}. ' \
               f'Мне уже {self.age} дней. ' \
               f'Мой пол - {self.gender.value}, я люблю хозяина фермы:)'
