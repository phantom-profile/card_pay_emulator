from farm import Farm
from interfaces import UserInterface
from database_managers import DatabaseManagerProtocol


class GameSession:
    def __init__(self, interface: UserInterface, database_manager: DatabaseManagerProtocol):
        self.ACTIONS = None
        self.interface = interface
        self.database_manager = database_manager
        self.user = database_manager.get_table_data('user')
        self.farm = database_manager.get_table_data('farm')
        self.init_menu()

    def start_game(self):
        if not self.user:
            self.user = self.interface.get_message({'username': 'Как тебя зовут?'})
            self.interface.send_message({'message': f'Добро пожаловать на ферму {self.user}'})
            self.farm = Farm(self.user)
        else:
            self.interface.send_message({'message': f'С возвращением на ферму, {self.user}!'})

        choice = ''
        while choice != '5':
            choice = self.make_choice()
            self.ACTIONS[choice]()

    def make_choice(self) -> str:
        choice = self.interface.get_message({'message': f'Чем займешься?'})
        while choice not in self.ACTIONS.keys():
            choice = self.interface.get_message({'message': f'Такого варианта нет, давай еще раз)'})
        return choice

    def add_new_animal(self):
        pass

    def remove_animal(self):
        pass

    def show_animals(self):
        self.interface.display_list(self.farm.animals)

    def show_menu(self):
        self.interface.send_message({'message': self.interface.MENU})

    def exit(self):
        self.interface.send_message({'message': f'Пока, {self.user}, все твои животные будут скучать!'})
        self.database_manager.save_table_data('user', self.user)
        self.database_manager.save_table_data('farm', self.farm)
        print(self.database_manager.get_table_data('user'))
        self.database_manager.close_session()

    def init_menu(self):
        self.ACTIONS = {
            '1': self.add_new_animal,
            '2': self.remove_animal,
            '3': self.show_animals,
            '4': self.show_menu,
            '5': self.exit,
        }
