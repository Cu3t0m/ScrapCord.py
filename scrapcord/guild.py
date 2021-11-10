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
from typing import Dict, List, Optional, TYPE_CHECKING

from .abc import DiscordModel
from .member import Member
from .role import Role
from . import utils

if TYPE_CHECKING:
    from .state import State
    from .types.guild import Guild as GuildPayload
    from .types.member import Member as MemberPayload
    from .types.role import RolePayload

class Guild(DiscordModel):
    """Represents a guild on Discord, often referred as a "Server" in the UI.

    Attributes
    ----------
    id: :class:`int`
        The unique snowflake ID of the guild.
    name: :class:`str`
        The name of guild.
    afk_timeout: :class:`int`
        The number of seconds after which idle members would be moved
        to the AFK channel. ``0`` means there is no timeout.
    widget_enabled: :class:`bool`
        Whether the guild has enabled embed widget.
    verification_level: :class:`VerificiationLevel`
        The verification level for the users of this guild.
    default_message_notifications: :class:`NotificationLevel`
        The message notification level of this guild.
    explicit_content_filter: :class:`ContentFilter`
        The explicit content filter of this guild. i.e if the sent media is scanned
        or not.
    features: :class:`str`
        The :class:`list` of the features this guild has, Guild features represent
        the features this guild has access to like role icons, welcome screen etc.
    mfa_level: :class:`MFALevel`
        The MFA level of this guild.
    application_id: Optional[:class:`int`]
        The ID of application that created this guild if it is bot created, This is usually
        ``None``
    large: Optional[:class:`bool`]
        Whether this guild is marked as a large guild. This is not available if the guild
        if fetched manually instead of getting from client's internal cache.
    unavailable: Optional[:class:`bool`]
        Whether this guild is unavailable due to an outage. This is not available if the guild
        if fetched manually instead of getting from client's internal cache.
    member_count: Optional[:class:`int`]
        The member count of this guild. This is not available if the guild
        if fetched manually instead of getting from client's internal cache.
    vanity_url_code: Optional[:class:`str`]
        The vanity URL code of this guild if any, Otherwise None.
    description: Optional[:class:`str`]
        The description of the guild. Could be None
    premium_tier: :class:`PremiumTier`
        The premium tier of this guild "aka" the server boost level.
    premium_subscription_count: :class:`int`
        The premium subscription count of this guild "aka" the number of boosts
        this guild has.
    preferred_locale: :class:`str`
        the preferred locale of a Community guild; used in server discovery and notices
        from Discord; Usually "en-US"
    approximate_member_count: :class:`int`
        The approximate member count of the guild, This is only available when
        fetching the guild using :meth:`~Client.fetch_guild` with ``with_counts`` parameter
        to ``True``
    approximate_presence_count: :class:`int`
        The approximate presences count of the guild, This is only available when
        fetching the guild using :meth:`~Client.fetch_guild` with ``with_counts`` parameter
        to ``True``
    nsfw_level: :class:`NSFWLevel`
        The NSFW level of the guild.
    """
    __slots__ = (
        'id', 'name', 'afk_timeout', 'widget_enabled', 'verification_level',
        'default_message_notifications', 'explicit_content_filter', 'features',
        'mfa_level', 'application_id', 'large', 'unavailable', 'member_count',
        'vanity_url_code', 'description', 'premium_tier', 'premium_subscription_count',
        'preferred_locale', 'approximate_member_count', 'approximate_presence_count',
        'nsfw_level', '_system_channel_id', '_rules_channel_id', '_public_updates_channel_id',
        '_afk_channel_id', '_roles', '_joined_at', '_owner_id', '_presences', '_system_channel_flags',
        '_icon', '_threads', '_emojis', '_voice_states', '_members', '_channels',
    )

    if TYPE_CHECKING:
        name: str
        afk_timeout: int
        widget_enabled: bool
        verification_level: int
        default_message_notifications: int
        explicit_content_filter: int
        features: List[str]
        mfa_level: int
        application_id: Optional[int]
        large: bool
        unavailable: bool
        member_count: int
        vanity_url_code: Optional[str]
        description: Optional[str]
        premium_tier: int
        premium_subscription_count: int
        preferred_locale: Optional[str]
        approximate_member_count: Optional[int]
        approximate_presence_count: Optional[int]
        nsfw_level: int
        _system_channel_id: Optional[int]
        _rules_channel_id: Optional[int]
        _public_updates_channel_id: Optional[int]
        _afk_channel_id: Optional[int]
        _joined_at: str
        _roles: Dict[int, Role]
        _owner_id: Optional[int]
        _presences: List[PresencePayload]
        _system_channel_flags: int
        _icon: str
        _emojis: Dict[int, Emoji]
        _voice_states: List[VoiceStatePayload]
        _channels: Dict[int, GuildChannel]
        _members: Dict[int, Member]

    def __init__(self, data: GuildPayload, state: State):
        self._state = state
        self._from_data(data)

    def _from_data(self, data: GuildPayload):
        self.id = int(data['id'])
        self.name = data['name']
        self.afk_timeout = data.get('afk_timeout', 0)
        self.widget_enabled = data.get('widget_enabled', False)
        self.verification_level = data.get('verification_level', 0)
        self.default_message_notifications = data.get('default_message_notifications', 0)
        self.explicit_content_filter = data.get('explicit_content_filter', 0)
        self.features = data.get('features', [])
        self.mfa_level = data.get('mfa_level', 0)
        self.application_id= data.get('application_id')
        self.large = data.get('large', False)
        self.unavailable = data.get('unavailable', False)
        self.member_count = data.get('member_count')
        self.vanity_url_code = data.get('vanity_url_code')
        self.description = data.get('description')
        self.premium_tier = data.get('premium_tier', 0)
        self.premium_subscription_count = data.get('premium_subscription_count', 0)
        self.preferred_locale = data.get('preferred_locale', "en-US")
        self.approximate_member_count = data.get('approximate_member_count')
        self.approximate_presence_count= data.get('approximate_presence_count')
        self.nsfw_level = data.get('nsfw_level', 0)

        # raw attributes
        self._system_channel_id = utils._get_snowflake(data, 'system_channel_id')
        self._rules_channel_id = utils._get_snowflake(data, 'rules_channel_id')
        self._public_updates_channel_id = utils._get_snowflake(data, 'public_updates_channel_id')
        self._afk_channel_id = utils._get_snowflake(data, 'afk_channel_id')
        self._joined_at = data.get('joined_at')
        self._owner_id = utils._get_snowflake(data, 'owner_id')
        self._presences = data.get('presences', [])
        self._system_channel_flags = data.get('system_channel_flags', 0)
        self._icon = data.get('icon')
        self._threads = data.get('threads', [])
        self._emojis  = data.get('emojis', [])
        self._voice_states = data.get('voice_states', [])

        self._channels = data.get('channels', [])

        self._members = {}
        self._roles = {}


        self._update_members(data.get('members', []))
        self._update_roles(data.get('roles', []))

        # self.region = data.get('region') # deprecated (use GuildChannel.rtc_region)
        # self.nsfw = data.get('nsfw', False) # deprecated (use nsfw level)

    @property
    def joined_at(self) -> datetime.datetime:
        """:class:`datetime.datetime`: Returns the datetime instance for the time when bot joined the guild."""
        if self.joined_at:
            return datetime.datetime.fromisoformat(self.joined_at)


    @property
    def members(self) -> List[Member]:
        """List[:class:`Member`]: Returns the list of members that are in this guild."""
        return list(self._members.values())

    def _update_members(self, members: List[MemberPayload]):
        for member in members:
            self._add_member(member)

    def _remove_member(self, id: int, /) -> Optional[Member]:
        return self._members.pop(id, None) # type: ignore

    def _add_member(self, data: MemberPayload) -> Optional[Member]:
        member = Member(data, state=self._state, guild=self)
        self._members[member.user.id] = member

        if not member.user.id in self._state.users:
            self._state.add_user(data['user'])

        return member

    def get_member(self, id: int, /) -> Optional[Member]:
        """Returns the member with the provided ID.

        This method would return ``None`` if no member
        is found with that ID.

        Parameters
        ----------
        id: :class:`int`
            The ID of required member.

        Returns
        -------
        Optional[:class:`Member`]
            The required member, if found.
        """
        return self._members.get(id) # type: ignore

    # roles management

    def _update_roles(self, roles: List[RolePayload]):
        for role in roles:
            self._add_role(role)

    def _add_role(self, role: RolePayload) -> Role:
        role = Role(role, guild=self)
        self._roles[role.id] = role
        return role

    def _remove_role(self, id: int, /) -> Optional[Role]:
        return self._roles.pop(id, None) # type: ignore

    def get_role(self, id: int, /):
        """Returns the role from this guild with the provided ID.

        This method would return ``None`` if no role
        is found with the provided ID.

        Parameters
        ----------
        id: :class:`int`
            The ID of required role.

        Returns
        -------
        Optional[:class:`Role`]
            The required role, if found.
        """
        return self._roles.get(id) # type: ignore

    @property
    def roles(self) -> List[Member]:
        """
        List[:class:`Role`]: Returns the list of roles that are in this guild.

        The list returned is sorted in a way so it's similar to how it is
        viewed in UI, The default role i.e @everyone role is always at the end of
        list.
        """
        # reversing the roles because it's in order:
        # @everyone
        # ...

        default_role = self.default_role
        roles = list(self._roles.values())

        # remove the default role and re-add it to
        # the end of list.
        roles.remove(default_role)
        roles.append(default_role)

        return roles

    @property
    def default_role(self) -> Role:
        """
        :class:`Role`: Returns the default i.e @everyone role of the guild.
        """
        # default role id is same as the guild id. This will
        # never be none.
        return self.get_role(self.id) # type: ignore

    @property
    def me(self) -> Member:
        """:class:`Member`: Returns the member that represent yourself's."""
        # this will not be none.
        return self.get_member(self._state.user.id) # type: ignore