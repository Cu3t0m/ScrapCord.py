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
from typing import Any, Set

class BaseFlags:
    VALID_FLAGS: Set[str]

    def __init__(self, value: Optional[int] = None, **flags: Any):
        invalid = set(flags.keys()) - set(self.VALID_FLAGS)
        if invalid:
            raise TypeError('Invalid keyword arguments {0} for {1}()'.format(invalid, self.__class__.__name__))

        if value:
            self._value = value
        else:
            self._value: int = sum([getattr(self.__class__, flag) for flag in flags if flags[flag] is True])

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, new: int) -> None:
        if not isinstance(new, int):
            raise TypeError('new value must be an int.')

        self._value = new

    def from_value(cls, value: int):
        raise NotImplementedError


class flag:
    def __init__(self, func: Callable[[], int]):
        self.func = func
        self.flag_val = func(None)

    def __get__(self, instance: Optional[BaseFlags], *_: Any):
        if not instance:
            return self.flag_val

        return (self.flag_val & instance.value)  == self.flag_val

    def __set__(self, instance: Optional[BaseFlags], val: bool):
        if not instance:
            return

        exists = (self.flag_val & instance.value)  == self.flag_val

        if val is False and exists:
            instance._value -= self.flag_val
        elif val is True and not exists:
            instance._value += self.flag_val

    def __repr__(self):
        return f'<flag value={self.flag_val}>'

class GatewayIntents(BaseFlags):
    """Represents the gateway intents.

    Intents allow you to choose to enable or disable certain events
    that you don't want or need to recieve over gateway.

    Following are the privileged intents that are required to be explicitly
    enabled from Discord Developer portal and require whitelisting if the bot
    if in over 100 guilds:

    - :attr:`GatewayIntents.members`
    - :attr:`GatewayIntents.presence`

    To see a brief list of events that would be recieved over gateway for
    certain intents, See the official
    `documentation`_ <https://discord.com/developers/docs/topics/gateway#gateway-intents>.

    Attributes
    ----------
    value: :class:`int`
        The raw integer value of the intents.
    """
    # (p): privileged
    VALID_FLAGS = {
        'guilds',
        'members', # (p)
        'bans',
        'emojis_and_stickers',
        'integrations',
        'webhooks',
        'invites',
        'voice_states',
        'presences', # (p)
        'guild_messages',
        'guild_messages_reactions',
        'guild_messages_typing',
        'direct_messages',
        'direct_messages_reactions',
        'direct_messages_typing',
    }
    def __init__(self, **intents):
        super().__init__(**intents)

    @classmethod
    def from_value(cls, value: int) -> GatewayIntents:
        """Constructs the :class:`GatewayIntents` from the raw value.

        Parameters
        ----------
        value: :class:`int`
            The raw value to construct intents with.

        Returns
        -------
        :class:`GatewayIntents`
            The constructed intents from the value.
        """
        # we want to bypass __init__ here so we would use __new__
        # and manually set the value.

        intents = cls.__new__(cls)
        intents._value = value
        return intents

    @classmethod
    def all(cls) -> GatewayIntents:
        """Constructs a :class:`GatewayIntents` with all intents enabled
        (including privileged ones).

        Returns
        -------
        :class:`GatewayIntents`
        """
        flags = {flag: True for flag in cls.VALID_FLAGS}
        return cls(**flags)

    @classmethod
    def unprivileged(cls) -> GatewayIntents:
        """Constructs a :class:`GatewayIntents` with all default intents enabled
        except privileged ones.

        Returns
        -------
        :class:`GatewayIntents`
        """
        intents = cls.all()
        intents.members = False
        intents.presences = False
        return intents

    @flag
    def guilds(self) -> int:
        """:class:`bool`: Returns ``True`` if the guild intents are enabled."""
        return 1 << 0

    @flag
    def members(self) -> int:
        """:class:`bool`: Returns ``True`` if the guild members intents are enabled.

        This is a privileged intent and must be explicitly enabled from Developers portal.
        If your bot is in more then 100 Guilds, you would require verification and
        intents whitelisting.
        """
        return 1 << 1

    @flag
    def bans(self) -> int:
        """:class:`bool`: Returns ``True`` if the guild bans intents are enabled."""
        return 1 << 2

    @flag
    def emojis_and_stickers(self) -> int:
        """:class:`bool`: Returns ``True`` if the emojis and stickers intents are enabled."""
        return 1 << 3

    @flag
    def integrations(self) -> int:
        """:class:`bool`: Returns ``True`` if the guild integrations intents are enabled."""
        return 1 << 4

    @flag
    def webhooks(self) -> int:
        """:class:`bool`: Returns ``True`` if the guild webhooks intents are enabled."""
        return 1 << 5

    @flag
    def invites(self) -> int:
        """:class:`bool`: Returns ``True`` if the guild invites intents are enabled."""
        return 1 << 6

    @flag
    def voice_states(self) -> int:
        """:class:`bool`: Returns ``True`` if the voice states intents are enabled."""
        return 1 << 7

    @flag
    def presences(self) -> int:
        """:class:`bool`: Returns ``True`` if the guild members presences intents are enabled."""
        return 1 << 8

    @flag
    def guild_messages(self) -> int:
        """:class:`bool`: Returns ``True`` if the guild messages intents are enabled."""
        return 1 << 9

    @flag
    def guild_messages_reactions(self) -> int:
        """:class:`bool`: Returns ``True`` if the guild message reactions intents are enabled."""
        return 1 << 10

    @flag
    def guild_messages_typing(self) -> int:
        """:class:`bool`: Returns ``True`` if the guild messages typing trigger intents are enabled."""
        return 1 << 11

    @flag
    def direct_messages(self) -> int:
        """:class:`bool`: Returns ``True`` if the direct messages intents are enabled."""
        return 1 << 12

    @flag
    def direct_messages_reactions(self) -> int:
        """:class:`bool`: Returns ``True`` if the direct message reactions intents are enabled."""
        return 1 << 13

    @flag
    def direct_messages_typing(self) -> int:
        """:class:`bool`: Returns ``True`` if the direct messages typing trigger intents are enabled."""
        return 1 << 14

class UserFlags(BaseFlags):
    """
    Represents the public flags of a user that appear on the user accounts.

    They are often referred as "badges" in the UI and are shown on the profile
    of users.

    This class should not be created manually.
    """
    VALID_FLAGS = {
        'discord_employee',
        'partnered_server_owner',
        'hypesquad_events',
        'bug_hunter_level_1',
        'house_bravery',
        'house_brilliance',
        'house_balance',
        'early_supporter',
        'team_user',
        'bug_hunter_level_2',
        'verified_bot',
        'early_verified_bot_developer',
        'discord_certified_moderator',
    }

    def __init__(self, value: int):
        super().__init__(value)

    @flag
    def discord_employee(self) -> int:
        """:class:`bool`: Returns ``True`` if the user is a Discord staff."""
        return 1 << 0

    @flag
    def partnered_server_owner(self) -> int:
        """:class:`bool`: Returns ``True`` if the user has the partnered server owner badge."""
        return 1 << 1

    @flag
    def hypesquad_events(self) -> int:
        """:class:`bool`: Returns ``True`` if the user has Hypesquad events badge."""
        return 1 << 2

    @flag
    def bug_hunter_level_1(self) -> int:
        """:class:`bool`: Returns ``True`` if the user has the level one of bug hunter badge."""
        return 1 << 3

    @flag
    def house_bravery(self) -> int:
        """:class:`bool`: Returns ``True`` if the user's house is HypeSquad Bravery."""
        return 1 << 6

    @flag
    def house_brilliance(self) -> int:
        """:class:`bool`: Returns ``True`` if the user's house is HypeSquad Brilliance."""
        return 1 << 7

    @flag
    def house_balance(self) -> int:
        """:class:`bool`: Returns ``True`` if the user's house is HypeSquad Balance."""
        return 1 << 8

    @flag
    def early_supporter(self) -> int:
        """:class:`bool`: Returns ``True`` if the user has the "Early Supporter" badge."""
        return 1 << 9

    @flag
    def team_user(self) -> int:
        """:class:`bool`: Returns ``True`` if user is a "team user"."""
        return 1 << 10

    @flag
    def bug_hunter_level_2(self) -> int:
        """:class:`bool`: Returns ``True`` if the has the user level two on bug hunter badge."""
        return 1 << 14

    @flag
    def verified_bot(self) -> int:
        """:class:`bool`: Returns ``True`` if the has the user is a verified bot."""
        return 1 << 16

    @flag
    def early_verified_bot_developer(self) -> int:
        """:class:`bool`: Returns ``True`` if the has the "Early Verified Bot Developer" badge."""
        return 1 << 17

    @flag
    def discord_certified_moderator(self) -> int:
        """:class:`bool`: Returns ``True`` if the has the "Certified Discord Moderator" badge."""
        return 1 << 18
