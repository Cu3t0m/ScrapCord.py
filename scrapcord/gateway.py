"""
MIT License

Copyright (c) 2021 ScrapCord

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from __future__ import annotations
from typing import TYPE_CHECKING

import threading
import sys
import zlib
import asyncio
import time
import json

if TYPE_CHECKING:
    from .client import Client
    from .flags import GatewayIntents

class OP:
    DISPATCH  = 0
    HEARTBEAT = 1
    IDENTIFY  = 2
    PRESENCE_UPDATE = 3
    VOICE_STATE_UPDATE = 4
    RESUME = 6
    RECONNECT = 7
    REQUEST_GUILD_MEMBERS = 8
    INVALID_SESSION = 9
    HELLO = 10
    HEARTBEAT_ACK = 11

class ReconnectDiscordWebsocket(Exception):
    pass

class HeartbeatHandler(threading.Thread):
    """
    A :class:`threading.Thread` that implements the logic of sending
    heartbeats to Discord to keep the websocket connection alive.
    """
    if TYPE_CHECKING:
        interval: Optional[int]

    def __init__(self, ws: DiscordWebsocket):
        self.ws = ws
        self.interval = None
        super().__init__(
            target=self._handler,
            daemon=True,
            name='scrapcord-heartbeat-handler'
            )

    def _handler(self):
        while not self.ws.is_closed():
            asyncio.run(
                self.ws.send_json({'op': OP.HEARTBEAT, 'd': self.ws.sequence}),
                )
            time.sleep(self.interval)

class DiscordWebsocket:
    """
    A class that implements the logic of handling the connection with
    Discord's gateway. This class is a private and internal class and must not
    be used.
    """
    if TYPE_CHECKING:
        session_id: Optional[str]
        sequence: Optional[int]
        heartbeat: HeartbeatHandler
        intents: GatewayIntents

    def __init__(self, client: Client):
        self.client = client
        self.intents = client.intents
        self.socket = None

        # websocket related data
        self.session_id = None
        self.sequence   = None
        self.heartbeat  = HeartbeatHandler(ws=self)
        self.inflator   = zlib.decompressobj()
        self.buffer     = bytearray()

    def is_closed(self):
        return self.socket and self.socket.closed

    async def receive_json(self):
        data = await self.socket.receive()
        data = data.data

        if isinstance(data, bytes):
            if len(data) < 4 or data[-4:] != b'\x00\x00\xff\xff':
                return

            data = inflator.decompress(self.buffer)
            self.buffer = bytearray()
            data = data.decode('utf-8')
        else:
            data = json.loads(data)

        return data

    async def send_json(self, data):
        await self.socket.send_str(json.dumps(data))

    async def start(self):
        """Establishes the websocket connection and starts sending packets."""
        url = await self.client.http.get_gateway()
        self.socket = await self.client.http.ws_connect(url)

        await self.handle_events()

    async def identify(self):
        payload = {
            "op": OP.IDENTIFY,
            "d": {
                "token": self.client.http.token,
                "intents": self.intents.value,
                "properties": {
                    "$os": sys.platform,
                    "$browser": "ScrapCord",
                    "$device": "ScrapCord"
                }
            }
        }
        await self.send_json(payload)

    async def handle_events(self):
        while not self.is_closed():
            msg = await self.receive_json()
            op = msg['op']
            data = msg['d']
            sequence = msg.get('s')

            if sequence:
                # store sequence for sending in heartbeats.
                self.sequence = sequence

            if op == OP.HELLO:
                # Here, We have got the HELLO OP code which means
                # we have to start heartbeating with the provided interval
                # and identify the session.

                self.heartbeat.interval = data['heartbeat_interval'] / 1000.0
                # we will send an immediate heartbeat here and start the heartbeat handler
                # thread.
                await self.send_json({'op': OP.HEARTBEAT, 'd': self.sequence})
                self.heartbeat.start()

                # we will now send the IDENTIFY packet.
                await self.identify()

            elif op == OP.HEARTBEAT:
                # we have got an heartbeat op code which means we have to
                # immediately heartbeat without waiting for heartbeat duration to reach
                await self.send_json({'op': OP.HEARTBEAT, 'd': self.sequence})

            elif op == OP.DISPATCH:
                event_name = msg['t']
                if event_name == 'READY':
                    # store session id to resume sessions later
                    self.session_id = data['session_id']

                self.client._state.process_event(event_name, data) # type: ignore

            elif op == OP.RECONNECT:
                raise ReconnectDiscordWebsocket()
