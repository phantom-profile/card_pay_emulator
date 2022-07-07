from animal import AnimalProtocol


class AnimalOnFarmException(Exception):
    def __init__(self, message):
        super().__init__()
        self.message = message


class Farm:
    def __init__(self, player_name: str):
        self.player_name = player_name
        self.animals: list[AnimalProtocol] = []

    def add_animal(self, animal: AnimalProtocol):
        self.animals.append(animal)

    def remove_animal(self, animal: AnimalProtocol):
        if animal not in self.animals:
            raise AnimalOnFarmException("Такого животного на ферме нет!")

        self.animals.remove(animal)

    def __str__(self) -> str:
        return f"Ферма игрока {self.player_name}"
