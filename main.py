import shelve

from game_session import GameSession
from database_managers import ShelveDatabaseManager
from interfaces import CLIUserInterface


def initialize_game() -> None:
    database = shelve.open("funny_farm_database")
    database_manager = ShelveDatabaseManager(database)
    game = GameSession(interface=CLIUserInterface(), database_manager=database_manager)
    game.start_game()


if __name__ == '__main__':
    initialize_game()
