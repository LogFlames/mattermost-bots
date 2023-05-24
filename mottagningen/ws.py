from asyncio import run
import websockets.client
from secret import TOKEN
from threading import Thread
import json

URI = "wss://mattermost.fysiksektionen.se:443/api/v4/websocket"
AUTH_SEND = json.dumps({ "seq": 1, "action": "authentication_challenge", "data": { "token": TOKEN}})


class WebSocket:
    def __init__(self):
        self.subscriptions = {}
        thread = Thread(target = self.start)
        thread.start()

    def subscribe(self, event, callback):
        if event not in self.subscriptions:
            self.subscriptions[event] = set()

        self.subscriptions[event].add(callback)

    def unsubscribe(self, event, callback):
        if event not in self.subscriptions:
            return

        if callback not in self.subscriptions[event]:
            return

        self.subscriptions[event].remove(callback)

    def start(self):
        run(self._connect())

    async def _connect(self):
        async with websockets.client.connect(URI) as websocket:
            await websocket.send(AUTH_SEND)
            while True:
                res = json.loads(await websocket.recv())
                if "event" in res and res["event"] in self.subscriptions and "data" in res:
                    for callback in self.subscriptions[res["event"]]:
                        callback(res["data"])

if __name__ == "__main__":
    WebSocket().start()
