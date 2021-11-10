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
from typing import Any, TYPE_CHECKING

from .abc import DiscordModel
from .asset import CDNAsset
from .color import Colour
from .flags import UserFlags
from .utils import MISSING
from . import utils

if TYPE_CHECKING:
    from .state import State

__all__ = ('User', 'ClientUser')

if TYPE_CHECKING:
    from .types.user import (
        User as UserPayload
    )

class BaseUser(DiscordModel):
    __slots__ = (
        'username', 'id', 'discriminator', 'bot', 'system',
        '_avatar', '_banner', '_accent_color', '_public_flags',
        '_state'
        )

    # TODO: Implement asset classes

    if TYPE_CHECKING:
        username: str
        discriminator: str
        bot: bool
        system: bool
        _avatar: str
        _banner: str
        _accent_color: str
        _public_flags: str

    def __init__(self, data: UserPayload, state: State):
        self._state = state
        self._from_data(data)

    def _from_data(self, data: UserPayload):
        self.username = data["username"]
        self.id = int(data["id"])
        self.discriminator = data["discriminator"]
        self.bot = data.get("bot", False)
        self.system = data.get("system", False)
        self._avatar = data.get("avatar", None)
        self._banner = data.get("banner", None)
        self._accent_colour = data.get("accent_color", None)
        self._public_flags = data.get("public_flags", 0)

    @property
    def accent_colour(self) -> Colour:
        """:class:`Colour`: Returns the colour representation of the user's accent colour."""
        if self._accent_colour is None:
            return Colour(0)

        return Colour(self._accent_colour)

    accent_color = accent_colour

    @property
    def public_flags(self) -> UserFlags:
        """:class:`UserFlags`: Returns the user public flags aka badges."""
        return UserFlags(self._public_flags)

    @property
    def default_avatar(self) -> CDNAsset:
        """:class:`CDNAsset`: Returns the CDN asset for user's default avatar.

        This doesn't represent the user's actual avatar but is calculated on
        the basis of user's discriminator.
        """
        return CDNAsset._from_default_avatar(self._state, self.discriminator)

    @property
    def avatar(self) -> Optional[CDNAsset]:
        """
        Optional[:class:`CDNAsset`]: Returns the asset for user's avatar. If
        user has no avatar, then ``None`` is returned instead.
        """
        if self._avatar is None:
            return self._avatar

        return CDNAsset._from_avatar(self._state, self.id, self._avatar)

    @property
    def banner(self) -> Optional[CDNAsset]:
        """
        Optional[:class:`CDNAsset`]: Returns the asset for user's profile banner. If
        user has no banner on profile, then ``None`` is returned instead.
        """
        if self._banner is None:
            return self._banner

        return CDNAsset._from_banner(self._state, self.id, self._banner)

    @property
    def mention(self) -> str:
        """:class:`str`: Returns a string used to mention the user within Discord."""
        return '<@!{0}>'.format(self.id)

    def is_me(self):
        """:class:`bool`: A boolean representing if the user is you i.e the connect client's user."""
        return self.id == self._state.user.id

    def __str__(self):
        return '{0}#{1}'.format(self.username, self.discriminator)

class ClientUser(BaseUser):
    """
    Represents a Discord User for the connected client. The most common
    way of accessing this is by :attr:`Client.user` attribute.

    Attributes
    ----------
    username: :class:`str`
        The username of user as shown in Discord.
    id: :class:`int`
        The user's unique snowflake ID.
    discriminator: :class:`str`
        The 4 digits discriminator of user.
    bot: :class:`bool`
        A boolean representing if the user is a bot or not, In case of this class
        this is usually ``True``
    system: :class:`bool`
        A boolean representing if the user is a system user i.e Official Discord System
        This is usually ``False``
    verified: :class:`bool`
        A boolean representing if the user has a verified email on the account.
    locale: Optional[:class:`str`]
        The language tag used to identify the language the user is using.
    mfa_enabled: :class:`bool`
        A boolean representing if the user has MFA enabled on the account.
    """
    if TYPE_CHECKING:
        verified: bool
        locale: Optional[str]
        mfa_enabled: bool

    def __init__(self, data: UserPayload, state: State):
        super().__init__(data, state)

    def _from_data(self, data: UserPayload):
        super()._from_data(data)

        # add additional non-common attributes
        self.verified = data.get('verified', False)
        self.locale = data.get('locale')
        self.mfa_enabled = data.get('mfa_enabled', False)

    async def edit(self, *,
        username: Optional[str] = MISSING,
        avatar: Optional[bytes] = MISSING
        ) -> ClientUser:

        """Edits the client user.

        Parameters
        ----------
        username: :class:`str`
            The new username.
        avatar: :class:`bytes`
            The bytes like object representing the new user's avatar. ``None`` denotes
            the removal of avatar. Supported image types are ``png`` and ``jpeg``

        Raises
        ------
        HTTPException:
            The editing of user failed.
        """
        payload = {}
        if username is not MISSING:
            payload['username'] = username
        if avatar is not MISSING:
            if avatar is None:
                payload['avatar'] = avatar
            else:
                payload['avatar'] = utils._get_image_data(avatar)

        if payload:
            new = await self._state.http.edit_client_user(payload=payload)
            self._from_data(new)
            self._state.user = self
            self._state.add_user(new)

        return self

class User(BaseUser):
    """
    Represents a "user entity" on Discord. A user may or may not share
    :class:`Guild` with you.

    Attributes
    ----------
    username: :class:`str`
        The username of user as shown in Discord.
    id: :class:`int`
        The user's unique snowflake ID.
    discriminator: :class:`str`
        The 4 digits discriminator of user.
    bot: :class:`bool`
        A boolean representing if the user is a bot or not, In case of this class
        this is usually ``True``
    system: :class:`bool`
        A boolean representing if the user is a system user i.e Official Discord System
        This is usually ``False``
    """
    def __init__(self, data: UserPayload, state: State):
        super().__init__(data, state)
