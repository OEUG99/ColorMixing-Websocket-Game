import random
from . import GameEntity, randomColor


class Food(GameEntity):
    def __init__(self):
        super().__init__(random.randint(-10000, 10000),
                         random.randint(-10000, 10000),
                         5,
                         randomColor())

    async def respawn(self):
        self.x = random.randint(-10000, 10000)
        self.y = random.randint(-10000, 10000)
