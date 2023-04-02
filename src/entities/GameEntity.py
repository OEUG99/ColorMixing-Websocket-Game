import random


def randomColor():
    r = random.randint(0, 3)
    if r == 0:
        return "red"
    elif r == 1:
        return "blue"
    elif r == 2:
        return "green"
    elif r == 3:
        return "white"


def blendColors(color1, color2):

    if color1 == color2:
        return color1

    if color2 == "white":
        return "white"

    if color1 == "white":
        return color2


    if color1 == "red" and color2 == "blue":
        return "purple"
    elif color1 == "blue" and color2 == "red":
        return "purple"
    elif color1 == "red" and color2 == "green":
        return "yellow"
    elif color1 == "green" and color2 == "red":
        return "yellow"
    elif color1 == "blue" and color2 == "green":
        return "cyan"
    elif color1 == "green" and color2 == "blue":
        return "cyan"
    elif color1 == "yellow" and color2 == "purple":
        return "black"
    elif color1 == "purple" and color2 == "yellow":
        return "black"
    else:
        return "black"


class GameEntity:
    def __init__(self, x, y, size, color):
        self.x = x
        self.y = y
        self.size = size
        self.color = color

    async def move(self, direction):
        pass

    async def check_collision(self, other):
        dx = self.x - other.x  # Calculate the difference in x coordinates
        dy = self.y - other.y  # Calculate the difference in y coordinates

        # Calculate the squared distance (sum of squared differences in x and y coordinates)
        squared_distance = dx ** 2 + dy ** 2

        # Calculate the actual distance by taking the square root of the squared distance
        distance = squared_distance ** 0.5

        # If the distance between the centers is less than or equal to the sum of their radii, they collide
        return distance <= self.size + other.size

    async def consume(self, other):
        pass

    async def kill(self):
        await self.respawn()

    async def respawn(self):
        self.x = random.randint(-1000, 10000)
        self.y = random.randint(-1000, 10000)
