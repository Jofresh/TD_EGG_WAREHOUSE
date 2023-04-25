from egg import Egg


class Warehouse:
    def __init__(self, capacity: int):
        self.__capacity = capacity
        self.eggs = []

    def get_capacity(self):
        return self.__capacity

    def get_eggs(self):
        return self.eggs

    def add_egg(self, egg: Egg):
        self.eggs.append(egg)

    def remove_egg(self, egg: Egg):
        self.eggs.remove(egg)

    def is_valid(self):
        if len(self.eggs) > self.__capacity:
            return False

        for egg in self.eggs:
            if not egg.is_valid():
                return False

        return True

    def __str__(self):
        return str(
            {"capacity": self.__capacity, "eggs": [str(egg) for egg in self.eggs]}
        )
