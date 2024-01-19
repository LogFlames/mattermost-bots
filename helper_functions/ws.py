from asyncio import run
import websockets.client
from threading import Thread
import json

class WebSocket:
    def __init__(self, TOKEN, print_events = False):
        self.URI = "wss://mattermost.fysiksektionen.se:443/api/v4/websocket"
        self.AUTH_SEND = json.dumps({ "seq": 1, "action": "authentication_challenge", "data": { "token": TOKEN}})
        self.subscriptions = {}
        self.thread = Thread(target = self.start)
        self.thread.start()
        self.print_events = print_events

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
        async with websockets.client.connect(self.URI, max_queue = 1024) as websocket:
            await websocket.send(self.AUTH_SEND)
            while True:
                res = json.loads(await websocket.recv())
                if "event" not in res:
                    continue
                
                if self.print_events:
                    print(res["event"])

                if res["event"] in self.subscriptions and "data" in res:
                    for callback in self.subscriptions[res["event"]]:
                        callback(res["data"])

    def join(self):
        self.thread.join()

if __name__ == "__main__":
    from secret import TOKEN
    WebSocket(TOKEN).join()
