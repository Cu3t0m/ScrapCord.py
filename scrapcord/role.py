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
from typing import TYPE_CHECKING, Optional

from . import utils
from .color import Colour
from .asset import CDNAsset
from .abc import DiscordModel

if TYPE_CHECKING:
    from .types.role import (
        Role as RolePayload,
        RoleTags as RoleTagsPayload,
    )
    from .state import State
    from .guild import Guild

MISSING = utils.MISSING

class RoleTags:
    """Represents the tags that are present on a role.

    Role tags contain information about the role's owner for example if a role is
    owned by an integration or if the role is a booster role.

    Attributes
    ----------
    bot_id: Optional[:class:`int`]
        The ID of the bot that owns this role. Could be None
    integration_id: Optional[:class:`int`]
        The ID of the integration that owns this role. Could be None
    """
    __slots__ = ('bot_id', 'integration_id', '_premium_subscriber')

    def __init__(self, data: RoleTagsPayload):
        self.bot_id = utils._get_snowflake(data, 'bot_id')
        self.integration_id = utils._get_snowflake(data, 'integration_id')

        # Discord API sends premium_subscriber field as null. If it is present
        # then it is True, if this is missing then it's False so we would
        # utils.MISSING

        self._premium_subscriber = data.get('premium_subscriber', MISSING)

    @property
    def premium_subscriber(self) -> bool:
        """
        :class:`bool`: Whether this role is for premium subscribers aka server boosters.

        Premium subscriber roles cannot be assigned or removed manually nor can it be
        deleted or created manually.
        """
        if self._premium_subscriber is MISSING:
            return False

        return True


class Role(DiscordModel):
    """Represents a role from a :class:`Guild`.

    A role can be assigned to guild members to modify their appearence in the UI or
    add certain permissions overwrites.

    Attributes
    ----------
    id: :class:`int`
        The unique snowflake ID of the role.
    name: :class:`str`
        The name of the role.
    hoist: :class:`bool`
        Whether the role is shown seperate from online members and other roles.
    position: :class:`int`
        An integer representing the position of the role in role heirarchy.
    managed: :class:`bool`
        Whether the role is managed by an integration.
    mentionable: :class:`bool`
        Whether the role is mentioned by members.
    unicode_emoji: Optional[:class:`str`]
        The string representation of the unicode emoji as role icon if any. This would
        be None if there is no unicode emoji on role icon.
    color: :class:`Colour`
        The color of the role.
    tags: :class:`RoleTags`
        The tags present on the role.
    """
    __slots__ = (
        '_guild', '_state', 'id', 'name', 'hoist', 'position',
        'managed', 'mentionable', 'unicode_emoji', 'color', 'tags',
        '_icon'
    )
    if TYPE_CHECKING:
        _guild: Guild
        _state: State
        id: int
        name: str
        hoist: bool
        position: int
        managed: bool
        mentionable: bool
        unicode_emoji: Optional[str]
        color: Colour
        tags: RoleTags
        _icon: Optional[str]

    def __init__(self, data: RolePayload, guild: Guild):
        self._guild = guild
        self._state = self._guild._state
        self._from_data(data)

    def _from_data(self, data: RolePayload):
        self.id = int(data['id'])
        self.name = data['name']
        self.hoist = data.get('hoist', False)
        self.position = int(data['position'])
        self.managed = data.get('managed', False)
        self.mentionable = data.get('mentionable', False)
        self.unicode_emoji = data.get('unicode_emoji')
        self.color = Colour(data.get('color', 0))
        self.tags = RoleTags(data.get('tags', {})) # type: ignore

        self._icon = data.get('icon')

    @property
    def guild(self):
        # this property is undocumented because it is unnecessary for
        # general use cases, it is manually exposed to the documentation
        # in events like role_update etc. where it is impossible to
        # figure out the guild the event occured in.
        return self._guild

    @property
    def icon(self) -> Optional[CDNAsset]:
        """
        Optional[:class:`CDNAsset`]: Returns the asset that represents the icon of this role.

        Could be None if role has no icon set.
        """
        if self._icon:
            return CDNAsset._from_icon(
                state=self._state,
                object_id=self.id,
                icon_hash=self._icon,
                path='role'
                )

    @property
    def mention(self) -> str:
        """:class:`str`: Returns a string used to mention the role in Discord."""
        return '<@&{0}>'.format(self.id)

    async def edit(self, *,
        name: Optional[str] = None,
        hoist: Optional[bool] = None,
        position: Optional[int] = None,
        mentionable: Optional[bool] = None,
        unicode_emoji: Optional[str] = MISSING,
        color: Optional[Colour] = MISSING,
        colour: Optional[Colour] = MISSING,
        icon: Optional[bytes] = MISSING,
        reason: str = None,
    ):
        """Edits the role.

        You need :attr:`Permissions.manage_roles` in role's guild to edit the role.

        Parameters
        ----------
        name: :class:`str`
        The name of the role.
        hoist: :class:`bool`
            Whether the role is shown seperate from online members and other roles.
        position: :class:`int`
            An integer representing the position of the role in role heirarchy.
        managed: :class:`bool`
            Whether the role is managed by an integration.
        mentionable: :class:`bool`
            Whether the role is mentioned by members.
        unicode_emoji: Optional[:class:`str`]
            The string representation of the unicode emoji as role icon if any. This could
            be None to remove the icon.
        color: :class:`Colour`
            The color of the role.
        icon: :class:`bytes`
            The bytes-like object representing the new icon, None can be passed to
            remove the icon.
        reason: :class:`str`
            The reason for editing the role, Shows up on the audit log.

        Raises
        ------
        Forbidden:
            You don't have permissions to edit the role.
        HTTPException:
            The editing of role failed somehow.
        """
        payload = {}
        if name is not None:
            payload['name'] = name
        if hoist is not None:
            payload['hoist'] = hoist
        if mentionable is not None:
            payload['mentionable'] = mentionable
        if unicode_emoji is not MISSING:
            payload['unicode_emoji'] = unicode_emoji
        if icon is not MISSING:
            if icon is None:
                payload['icon'] = icon
            else:
                payload['icon'] = utils._get_image_data(icon)


        if color is not MISSING or colour is not MISSING:
            if color is not MISSING:
                payload['color'] = color.value
            elif colour is not MISSING:
                payload['color'] = colour.value

        if payload:
            data = await self._state.http.edit_role(
                guild_id=self._guild.id,
                role_id=self.id,
                reason=reason,
                payload=payload,
                )

        if position is not None:
            payload = {'position': position, 'id': self.id}
            roles = await self._state.http.edit_role_position(
                guild_id=self._guild.id,
                payload=payload,
                reason=reason,
                )

    async def delete(self, *, reason: Optional[str] = None):
        """Deletes the role.

        Parameters
        ----------
        reason: :class:`str`
            The reason for deleting the role; Shows up on audit log.

        Raises
        ------
        Forbidden:
            You don't have permissions to delete the role.
        HTTPException:
            The deletion of role failed somehow.
        """
        await self._state.http.delete_role(
            guild_id=self.guild.id,
            role_id=self.id,
            reason=reason,
        )
