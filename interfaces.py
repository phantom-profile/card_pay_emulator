from typing import Protocol, Any
from animal import Displayable


class UserInterface(Protocol):
    MENU: str

    def send_message(self, serialized_message: dict[str, Any]) -> None: ...

    def get_message(self, serialized_message: dict[str, Any]) -> str: ...

    def display_list(self, objects_to_display: list[Displayable]) -> None: ...

    def fill_form(self, empty_form: dict[str, None]) -> dict[str, str]: ...


class CLIUserInterface:
    MENU = """
        1 - добавить животное на ферму
        2 - убрать животное с фермы
        3 - показать всех животных на ферме
        4 - показать это меню
        5 - завершить игру
    """

    @staticmethod
    def send_message(message: dict[str, Any]):
        for value in message.values():
            print(value)

    @staticmethod
    def get_message(message: dict[str, Any]):
        response: str = ''
        for value in message.values():
            while not response.strip():
                response = input(value)
        return response.strip()

    @staticmethod
    def display_list(objects_to_display: list[Displayable]):
        print(f"Общее количество: {len(objects_to_display)}")

        for displayable in objects_to_display:
            print(displayable)

    @staticmethod
    def fill_form(empty_form: dict[str, None]) -> dict[str, str]:
        filled_form = {}
        for key, in empty_form.keys():
            filled_form[key] = input(f'Fill in value for {key}')

        return filled_form
