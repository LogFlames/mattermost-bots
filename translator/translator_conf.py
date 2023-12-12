from typing import Literal
from dataclasses import dataclass

class TranslateChannelsConf:
    def __init__(self):
        self.channels = {}

    def add_channel(self, name, channel_id, add_to_events, send_reply: Literal["reply", "dm"]):
        self.channels[channel_id] = ChannelSettings(name = name, channel_id = channel_id, add_to_events = add_to_events, send_reply = send_reply)

@dataclass
class ChannelSettings:
    name: str
    channel_id: str
    add_to_events: bool
    send_reply: Literal["reply", "dm"]
