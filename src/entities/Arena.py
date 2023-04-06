import json
import bson
import uuid

from src.entities import Player


class Arena:

    def __init__(self, socketHandler):
        self.entities = {}
        self.currentID = 0
        self.socketHandler = socketHandler

    async def addEntity(self, entity):
        self.currentID += 1
        self.entities[self.currentID] = entity

        if isinstance(entity, Player):
            # Send all entities to new player
            await self.updateView("init", self.entities, room=entity.sid)
            # Send new entity to all players
            await self.updateView(obj={self.currentID: entity}, room=None, skip_sid=entity.sid)
            print(f'Player added - UUID: {self.currentID}')
            return

        print(f'Entity added - UUID: {self.currentID}')

        # Send new entity to all players
        # await self.updateView(entity)

    async def removeEntity(self, entity):
        self.entities.pop(entity.id)

    async def getEntity(self, UUID):
        return self.entities[UUID]

    async def serialize(self, obj=None, ):

        async def object_to_dict(obj):
            if hasattr(obj, '__dict__'):
                return obj.__dict__
            # Additional handling for other custom classes if needed
            return obj

        action = "partial_update"

        if obj is None or obj is self.entities:
            obj = self.entities
            action = "full_update"

        # Create an empty dictionary to store the serialized data
        serialized_data = {}

        # Ensure obj is a dictionary
        if not isinstance(obj, dict):
            obj = await object_to_dict(obj)

        # Iterate through the keys and values in the input dictionary
        for key, value in obj.items():
            # Check if the value is a dictionary
            if isinstance(value, dict):
                # If the value is a dictionary, recursively call the serialize method
                serialized_data[key] = self.serialize(value)
            else:
                # Convert the value to a dictionary if possible
                serialized_value = await object_to_dict(value)
                # Add the serialized value to the serialized_data dictionary
                serialized_data[key] = serialized_value

        # Return the serialized data along with the action
        output = {"action": action, "data": serialized_data}

        return bson.dumps(output)

    # mirrors emitMessage but written to support automatic seralization
    async def updateView(self, type='update', obj=None, room=None, skip_sid=None):
        await self.socketHandler.emitMessage(type, await self.serialize(obj), room, skip_sid)