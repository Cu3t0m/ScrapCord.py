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
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING

import inspect
import asyncio

from .gateway import DiscordWebsocket, ReconnectDiscordWebsocket, OP
from .state import State
from .flags import GatewayIntents
from .user import User

if TYPE_CHECKING:
    from .http import HTTPClient
    from .user import ClientUser

class Client:
    """
    Represents a client that connects to the Discord's websocket and
    interacts with the API. This class is starting point of almost any bot.

    This class takes *no required arguments* but certain keyword arguments
    can be passed to customize the behaviour of the bot.

    .. note::
        All parameters are keyword only and optional.

    Parameters
    ----------
    session: :class:`aiohttp.ClientSession`
        The aiohttp session that will be internally be used. If not provided, Library
        creates it's own session.
    """
    if TYPE_CHECKING:
        _ws: DiscordWebsocket
        _state: State
        listeners: Dict[str, Callable[..., Any]]
        intents: Intents
        loop: asyncio.AbstractEventLoop

    def __init__(self, **options: Any):
        self.intents = options.get('intents', GatewayIntents.unprivileged())

        # internal stuff
        self.listeners = {}
        self.loop = options.get('loop') or asyncio.get_event_loop()
        self._ws = DiscordWebsocket(client=self)
        self._state = State(dispatch=self.dispatch, session=options.get('session'))
        self._state._get_client = lambda: self # type: ignore

    @property
    def http(self) -> HTTPClient:
        return self._state.http

    async def connect(self, token: str, /) -> None:
        """
        Connects to Discord's websocket with the provided token.

        Parameters
        ----------
        token: :class:`str`
            The bot's auth token. This is a positional only argument.
        """
        self._state.http.token = token
        try:
            await self._ws.start()
        except ReconnectDiscordWebsocket:
            _log.info('Got a signal to reconnect the websocket, Attempting to RESUME')

            session_id = self.ws.session_id
            sequence = self.ws.sequence

            if not self.ws.socket.closed:
                # this reminds me of "we will be right back" lol
                await self.ws.socket.close(1000)

            self.ws.heartbeat.stop()

            await self.connect(token)

            # finally, resuming the session...
            await self.ws.send_json({
                "op": OP.RESUME,
                "d": {
                    "token": token,
                    "session_id": session_id,
                    "seq": sequence,
                }
            })

    # listeners management

    def add_listener(self, listener: Callable[..., Any], name: Optional[str] = None) -> Callable[..., Any]:
        """Adds an event listener to the bot. This is a non-decorator
        interface to :meth:`.listener` decorator which should be used instead.

        Example::

            async def on_message(message):
                ...

            bot.add_listener(on_message)

        Parameters
        ----------
        listener:
            The async function that represents the event's callback.
        """
        if not inspect.iscoroutinefunction(listener):
            raise TypeError('listener callback must be a coroutine.')

        if not name:
            name = listener.__name__

        if not name.startswith('on_'):
            raise TypeError('Listener name must be followed by "on_"')

        name = name[3:] # remove the "on_" from the name

        try:
            self.listeners[name].append(listener)
        except KeyError:
            self.listeners[name] = [listener]

        return listener

    def clear_listeners(self, event: str):
        """Removes all the listeners for an event. This method would
        suppress error if the no listener is present for provided event.

        Parameters
        ----------
        event: :class:`str`
            The event's name whose listeners should be removed. Like ``on_message``
        """
        if event.startswith('on_'):
            event = event[3:]

        try:
            del self.listeners[event]
        except KeyError:
            pass

    def listener(self, *args):
        """A decorator interface for registering event listeners.

        Example::

            @bot.listener
            async def on_ready():
                print('Bot is ready.')
        """
        def decorator(coro):
            return self.add_listener(coro, *args)

        return decorator

    def dispatch(self, event: str, *args: Any):
        listeners = self.listeners.get(event, [])

        for listener in listeners:
            self._schedule_event(listener, *args)

    def _schedule_event(self, coro: Coroutine[..., Any], *args: Any) -> asyncio.Task:
        wrap = coro(*args)
        return asyncio.create_task(wrap, name=f'scrapcord-event-dispatch: {coro.__name__[:3]}')

    # properties

    @property
    def user(self) -> ClientUser:
        """:class:`ClientUser`: Returns the user that belongs to the client "aka" your bot."""
        return self._state.user

    @property
    def users(self) -> List[User]:
        """List[:class:`User`]: Returns the list of users that the client can see.

        .. note::
            If :attr:`GatewayIntents.members` are disabled, this list would most likely
            contain only one user that would be your :class:`ClientUser`
        """
        return self._state.users

    # getters & fetchers

    # users

    def get_user(self, id: int, /) -> Optional[User]:
        """Gets a :class:`User` from the client's internal cache.

        This method would return ``None`` if user is not found in cache.

        .. note::
            If :attr:`GatewayIntents.members` are disabled, This method would
            return ``None`` in most cases.

        Parameters
        ----------
        id: :class:`int`
            The ID of user to get

        Returns
        -------
        Optional[:class:`User`]
            The resolved user, if found.
        """
        return self._state.get_user(id)

    async def fetch_user(self, id: int, /) -> User:
        """Fetches a :class:`User`

        This method is an API call, for general usage, Consider using :meth:`.get_user`
        instead.

        Parameters
        ----------
        id: :class:`int`
            The ID of user to fetch.

        Returns
        -------
        :class:`User`
            The fetched user.

        Raises
        ------
        NotFound:
            The provided user ID is invalid.
        HTTPException:
            The fetching of user failed.
        """
        user = await self.http.get_user(id)
        return User(user, state=self._state)

    # guilds management

    def get_guild(self, id: int, /) -> Optional[Guild]:
        """Gets a :class:`Guild` from the client's internal cache.

        This method would return ``None`` if guild is not found in cache.

        .. note::
            If :attr:`GatewayIntents.guilds` are disabled, This method would
            return ``None`` in most cases.

        Parameters
        ----------
        id: :class:`int`
            The ID of guild to get

        Returns
        -------
        Optional[:class:`Guild`]
            The resolved guild, if found.
        """
        return self._state.get_guild(id)