import random
from . import BaseEntity, randomColor


class Food(BaseEntity):
    def __init__(self):
        super().__init__(random.randint(-2000, 2000),
                         random.randint(-2000, 2000),
                         4,
                         randomColor())

    async def respawn(self):
        self.x = random.randint(-2000, 2000)
        self.y = random.randint(-2000, 2000)
