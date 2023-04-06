import asyncio

from aiohttp import web
import aiohttp_jinja2
import jinja2
from src.entities.Player import Player
from network.SocketHandler import socketHandler
from entities.Arena import Arena

app = socketHandler.app
sio = socketHandler.sio

# Set up Jinja2 environment for aiohttp
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(['templates']))

players = {}  # A dictionary to store players' state
entities = {}  # A dictionary to store entities' state

arena = Arena(socketHandler)


@aiohttp_jinja2.template('index.html')
async def index(request):
    return {}


@sio.event
async def connect(sid, environ):
    await arena.addEntity(Player(sid))
    print(f'Client connected - SID: {sid}')


@sio.event
async def player_disconnect(sid):
    print('Client disconnected')


app.router.add_get('/', index)

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=8005)
