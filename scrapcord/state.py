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
from typing import Dict, Any, TYPE_CHECKING

from .http import HTTPClient
from .user import User, ClientUser
from .guild import Guild
from .member import Member
from . import utils

import time
import copy

if TYPE_CHECKING:
    from .client import Client
    from .types.user import User as UserPayload
    from .types.guild import Guild as GuildPayload

EventData = Dict[str, Any]

class State:
    """
    A class that implements the state management and handling of gateway events.
    This class is private and should not be initalized manually.
    """
    if TYPE_CHECKING:
        http: HTTPClient
        user: ClientUser
        _get_client: Callable[[], Client]
        users: Dict[int, User]
        guilds: Dict[int, Guild]

    def __init__(self, *, dispatch: Callable[[str, ...], Any], session: ClientSession):
        self.dispatch = dispatch
        self.http = HTTPClient(session=session)
        self.user = None
        self.clear()

    def clear(self):
        self.users  = {}
        self.guilds = {}

    # users management

    def get_user(self, id: int, /):
        return self.users.get(id)

    def add_user(self, data: UserPayload):
        user = User(data, state=self)
        self.users[int(data['id'])] = user
        return user

    def remove_user(self, id: int, /):
        return self.users.pop(id, None) # type: ignore

    # guilds management

    def get_guild(self, id: int, /):
        return self.guilds.get(id)

    def add_guild(self, data: GuildPayload):
        guild = Guild(data, state=self)
        self.guilds[int(data['id'])] = guild
        return guild

    def remove_guild(self, id: int, /):
        return self.guilds.pop(id, None) # type: ignore

    # event handlers

    def process_event(self, name: str, data: EventData):
        handler = getattr(self, f'handle_{name.lower()}', None)
        if handler:
            handler(data)

    def handle_ready(self, data: EventData):
        self.user = ClientUser(data['user'], state=self)
        self.add_user(data['user'])

        # TODO: Figure out a good way to dispatch
        # ready only when the cache is filled.
        self.dispatch('ready')

    def handle_user_update(self, data: EventData):
        user = self.get_user(int(data['id']))
        if not user:
            return

        before = copy.copy(user)
        user._from_data(data)
        self.dispatch('user_update', before, user)

    def handle_guild_create(self, data: EventData):
        unavailable = data.get('unavailable')
        if unavailable:
            return

        guild = self.add_guild(data)

        if unavailable is False:
            self.dispatch("guild_available", guild)

        self.dispatch('guild_join', guild)

    def handle_guild_update(self, data: EventData):
        guild = self.get_guild(int(data['id']))
        if not guild:
            return

        before = copy.copy(guild)
        guild._from_data(data)
        self.dispatch('guild_update', before, guild)


    def handle_guild_delete(self, data: EventData):
        unavailable = data.get('unavailable')
        guild = self.remove_guild(int(data['id']))

        if not unavailable:
            # user has been removed from guild
            self.dispatch('guild_leave', guild)

    def handle_guild_member_add(self, data: EventData):
        guild_id = utils._get_snowflake(data, 'guild_id')
        guild = self.get_guild(guild_id)

        if not guild:
            # unknown guild
            return

        member = guild._add_member(data) # type: ignore
        self.dispatch('member_join', member)

    def handle_guild_member_remove(self, data: EventData):
        guild_id = utils._get_snowflake(data, 'guild_id')
        guild = self.get_guild(guild_id)

        if not guild:
            # unknown guild
            return

        user = User(data, state=self)
        guild._remove_member(user.id) # type: ignore

        self.dispatch('member_remove', user)


    def handle_guild_member_update(self, data: EventData):
        guild_id = utils._get_snowflake(data, 'guild_id')
        guild = self.get_guild(guild_id)

        if not guild:
            # unknown guild
            return

        before = copy.copy(guild.get_member(int(data['user']['id'])))
        after = guild._add_member(data)
        self.dispatch('member_update', before, after)

    def handle_guild_role_create(self, data: EventData):
        guild_id = utils._get_snowflake(data, 'guild_id')
        guild = self.get_guild(guild_id)
        if not guild:
            return

        role = guild._add_role(data['role'])
        self.dispatch('role_create', role)

    def handle_guild_role_delete(self, data: EventData):
        guild_id = utils._get_snowflake(data, 'guild_id')
        guild = self.get_guild(guild_id)
        if not guild:
            return

        role_id = utils._get_snowflake(data, 'role_id')
        role = guild._remove_role(role_id)

        if not role:
            return

        self.dispatch('role_delete', role)

    def handle_guild_role_update(self, data: EventData):
        guild_id = utils._get_snowflake(data, 'guild_id')
        guild = self.get_guild(guild_id)
        if not guild:
            return

        role = guild.get_role(int(data['role']['id']))
        if not role:
            # role doesn't exist; add it.
            role = guild._add_role(role)
        before = copy.copy(role)


        role._from_data(data['role'])
        self.dispatch('role_update', before, role)

