import asyncio
import math
import random
import threading
from .Food import Food
from .GameEntity import GameEntity, randomColor, blendColors


class Player(GameEntity):
    def __init__(self):
        super().__init__(random.randint(0, 800),
                         random.randint(0, 400), 5, randomColor())
        self.cooldown = False
        self.velocity = 15


    async def move(self, direction):
        if direction == 'up':
            self.y -= self.velocity

        elif direction == 'down':
            self.y += self.velocity

        elif direction == 'left':
            self.x -= self.velocity

        elif direction == 'right':
            self.x += self.velocity

        elif direction == 'space':
            await self.useAbility()

    async def moveViaMouse(self, angle):
        self.x += self.velocity * math.cos(angle)
        self.y += self.velocity * math.sin(angle)

    async def consume(self, other):

        if isinstance(other, Player):
            if self.size > other.size:
                self.size = max(self.size + other.size, 100)
                self.color = blendColors(self.color, other.color)
                await other.kill()
            else:
                other.size = max(self.size + other.size, 100)
                other.color = blendColors(self.color, other.color)
                await self.kill()
        elif isinstance(other, Food):
            self.size = max(self.size + other.size, 100)
            self.color = blendColors(self.color, other.color)
            await other.kill()
        else:
            print("Can't consume unknown entity {}!".format(type(other)))

    async def useAbility(self):
        if self.color == "purple":
            if not self.cooldown:
                self.cooldown = True
                self.size = random.randint(5, int(self.size*2))
                await asyncio.sleep(120)
                self.velocity = 15
                self.cooldown = False
        elif self.color == "yellow":
            if not self.cooldown:
                self.cooldown = True
                self.velocity = 30
                self.size -= int(self.size/4)
                await asyncio.sleep(8)
                self.velocity = 15
                self.cooldown = False
        elif self.color == "cyan":
            if not self.cooldown:
                self.cooldown = True
                self.x += random.randint(-50, 500)
                self.y += random.randint(-50, 500)
                self.size = min(self.size - self.size/4, 5)
                await asyncio.sleep(15)
                self.velocity = 15
                self.cooldown = False


    async def respawn(self):
        self.x = random.randint(0, 800)
        self.y = random.randint(0, 400)
        self.size = 5
        self.velocity = 15
        self.color = randomColor()
        self.cooldown = False
