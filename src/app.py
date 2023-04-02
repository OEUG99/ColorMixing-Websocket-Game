import math
import os
import random
import asyncio
from aiohttp import web
import socketio
import aiohttp_jinja2
import jinja2
from entities.Player import Player
from entities.Food import Food

sio = socketio.AsyncServer(async_mode='aiohttp')
app = web.Application()
sio.attach(app)

# Set up Jinja2 environment for aiohttp
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))

players = {}  # A dictionary to store players' state
entities = {}  # A dictionary to store entities' state

# Create a bunch of entities
for i in range(200):
    entities[i] = Food()


@aiohttp_jinja2.template('index.html')
async def index(request):
    return {}


@sio.event
async def connect(sid, environ):
    player_id = sid
    players[player_id] = Player()
    await broadcast_update()
    print(f'Client connected - SID: {player_id}')

@sio.event
async def disconnect(sid):
    player_id = sid
    del players[player_id]
    print('Client disconnected')
    await broadcast_update()

async def handle_collisions(player_id, player):
    tasks = []
    for other_id, other_player in players.items():
        if player_id != other_id:
            tasks.append(player.check_collision(other_player))

    collisions = await asyncio.gather(*tasks)
    for idx, collision in enumerate(collisions):
        if collision:
            other_id = list(players.keys())[idx]
            other_player = players[other_id]
            await player.consume(other_player)
            break

    tasks = []
    for entity_id, entity in entities.items():
        tasks.append(player.check_collision(entity))

    collisions = await asyncio.gather(*tasks)
    for idx, collision in enumerate(collisions):
        if collision:
            entity_id = list(entities.keys())[idx]
            entity = entities[entity_id]
            await player.consume(entity)
            entities.pop(entity_id)
            break

async def process_movement(player_id, player, direction=None):
    await player.move(direction)

    await handle_collisions(player_id, player)
    players[player_id] = player
    await broadcast_update()

@sio.event
async def player_arrow_movement(sid, data):
    player_id = sid
    player = players[player_id]
    direction = data
    await process_movement(player_id, player, direction=direction)

async def broadcast_update():
    players_list = [{'id': player_id, **player.__dict__} for player_id, player in players.items()]
    entities_list = [{'id': entity_id, **entity.__dict__} for entity_id, entity in entities.items()]
    await sio.emit('update', {'players': players_list, 'entities': entities_list}, room=None)

app.router.add_get('/', index)

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=80)
