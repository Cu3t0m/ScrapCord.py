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
from typing import TypedDict, Literal, Optional

from .snowflake import Snowflake
from .role import Role
from .emoji import Emoji
from .welcome_screen import WelcomeScreen
from .sticker import Sticker
from .stage import StageInstance
from .user import User
from .member import Member
from .voice import VoiceState

VerificationLevel = Literal[0, 1, 2, 3, 4]
NotificationLevel = Literal[0, 1]
ExplicitContentFilter = Literal[0, 1, 2]
MFALevel = Literal[0, 1]
PremiumTier = Literal[0, 1, 2, 3]
NSFWLevel = [0, 1, 2, 3]

class _GuildOptional(TypedDict, total=False):
    icon_hash: Optional[str]
    owner: bool
    permissions: str
    region: str
    widget_enabled: bool
    widget_channel_id: Optional[Snowflake]
    joined_at: str
    large: bool
    unavailable: bool
    member_count: bool
    voice_states: List[VoiceState]
    members: List[Member]
    channels: List[GuildChannel] # type: ignore
    threads: List[GuildChannel] # type: ignore
    presences: List[PresenceUpdate] # type: ignore
    max_presences: int
    max_members: int
    max_video_channel_users: int
    approximate_member_count: int
    approximate_presence_count: int
    welcome_screen: WelcomeScreen
    stage_instances: List[StageInstance]
    stickers: List[Sticker]

class Guild(_GuildOptional):
    id: Snowflake
    name: str
    icon: Optional[str]
    splash: Optional[str]
    discovery_splash: Optional[str]
    owner_id: Snowflake
    afk_channel_id: Optional[Snowflake]
    afk_timeout: int
    verification_level: VerificiationLevel
    default_message_notifications: NotificationLevel
    explicit_content_filter: ExplicitContentFilter
    roles: List[Role]
    emojis: List[Emoji]
    features: List[str]
    mfa_level: MFALevel
    application_id: Optional[Snowflake]
    system_channel_id: Optional[Snowflake]
    system_channel_flags: int
    rules_channel_id: Optional[Snowflake]
    description: str
    banner: str
    premium_tier: PremiumTier
    premium_subscription_count: int
    preferred_locale: str
    public_updates_channel_id: Optional[Snowflake]
    nsfw_level: NSFWLevel
