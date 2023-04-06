import socketio
from aiohttp import web


class SocketHandler:

    def __init__(self):
        self.sio = socketio.AsyncServer(async_mode='aiohttp')
        self.app = web.Application()
        self.sio.attach(self.app)

    async def emitMessage(self, event, data, room=None, skip_sid=None):
        await self.sio.emit(event, data, room=room, skip_sid=skip_sid)


# we will use a single instance across the app
# though since this isn't a singleton, we can have multiple instances if we want
socketHandler = SocketHandler()
