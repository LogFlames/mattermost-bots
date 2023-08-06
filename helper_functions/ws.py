from asyncio import run
import websockets.client
from threading import Thread
import json

class WebSocket:
    def __init__(self, TOKEN):
        self.URI = "wss://mattermost.fysiksektionen.se:443/api/v4/websocket"
        self.AUTH_SEND = json.dumps({ "seq": 1, "action": "authentication_challenge", "data": { "token": TOKEN}})
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
        async with websockets.client.connect(self.URI) as websocket:
            await websocket.send(self.AUTH_SEND)
            while True:
                res = json.loads(await websocket.recv())
                if "event" in res and res["event"] in self.subscriptions and "data" in res:
                    for callback in self.subscriptions[res["event"]]:
                        callback(res["data"])

if __name__ == "__main__":
    from secret import TOKEN
    WebSocket(TOKEN).start()
