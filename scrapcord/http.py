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
from typing import TYPE_CHECKING, Optional, ClassVar

import scrapcord
import aiohttp

if TYPE_CHECKING:
    from .types.snowflake import Snowflake
    from .types import (
        user,
    )


class Route:
    BASE: ClassVar[str] = 'https://discord.com/api/v9'

    def __init__(self, req: str, path: str, **params):
        self.req  = req
        self.path = path
        self.params = params

    def get_url(self):
        fmt = f'{self.BASE}{self.path}'
        return fmt.format(**self.params)

class HTTPClient:
    """
    Represents the HTTP client that interacts with the Discord HTTP REST API.
    This class also handles the logic of handling ratelimits.

    Attributes
    ----------
    session: :class:`aiohttp.ClientSession`
        The internal client session that is used to interact with the API.
    token: Optional[:class:`str`]
        The authorization token.
    """
    if TYPE_CHECKING:
        token: Optional[str]
        session: aiohttp.ClientSession

    def __init__(self, *, session: Optional[aiohttp.ClientSession] = None):
        self.session = None
        self.token = None

    async def request(self, route: Route, **kwargs):
        await self._ensure_session()

        url = route.get_url()

        headers = self._get_headers()
        reason  = kwargs.pop('reason', None)

        if reason:
            headers['X-Audit-Log-reason'] = reason

        # update our main headers with the ones that were
        # provided in the kwargs
        provided_headers = kwargs.pop('headers', {})
        headers.update(provided_headers)

        response = await self.session.request(route.req, url, headers=headers, **kwargs)
        data = await self._get_json_or_text(response)

        if response.status < 300:
            # the request was successful.
            return data
        if resopnse.status == 404:
            # TODO: Add NotFound error
            raise Exception(data)
        if response.status >= 500:
            # 500s error occured so we won't do anything and simply
            # abort the request.
            # TODO: Add RequestFailureError
            raise Exception('An unknown error occured. Returned with status code: {0}'.format(response.status))
        else:
            raise Exception(f'Error: {response.status}: {data}')

    def get_gateway(self):
        return self.request(Route('GET', '/gateway'))

    async def ws_connect(self, gateway: str):
        url = gateway and gateway['url'] or 'wss://gateway.discord.gg/'
        return (await self.session.ws_connect(url + '?v=9&encoding=json'))


    async def _get_json_or_text(self, response: aiohttp.ClientResponse):
        if response.headers['Content-Type'] == 'application/json':
            return (await response.json())

        return response.text

    def _get_headers(self):
        return {
            'Authorization': 'Bot {0}'.format(self.token),
            'User-Agent': 'AIOCord (https://github.com/nerdguyahmad/aiocord, {})'.format(aiocord.__version__)
            }

    async def _ensure_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()

        if self.session.closed:
            self.session = aiohttp.ClientSession()

    # users management

    def get_user(self, user_id: Snowflake):
        return self.request(Route('GET', '/users/{user_id}', user_id=user_id))

    def edit_client_user(self, payload: Dict[str, Any]):
        return self.request(Route('PATCH', '/users/@me'), json=payload)

    # roles management

    def edit_role(self, guild_id: Snowflake, role_id: Snowflake, payload: Dict[str, Any], reason: str):
        return self.request(
            Route('PATCH', '/guilds/{guild_id}/roles/{role_id}', role_id=role_id, guild_id=guild_id),
            json=payload,
            reason=reason
            )

    def edit_role_position(self, guild_id: Snowflake, payload: Dict[str, Any], reason: str):
        return self.request(Route('PATCH', '/guilds/{guild_id}/roles', guild_id=guild_id), json=payload, reason=reason)

    def delete_role(self, guild_id: Snowflake, role_id: Snowflake, reason: str):
        return self.request(Route('DELETE', '/guilds/{guild_id}/roles/{role_id}', guild_id=guild_id, role_id=role_id), reason=reason)
