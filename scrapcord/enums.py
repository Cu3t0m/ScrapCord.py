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

class PremiumType:
    """
    An enumeration that details the types of a premium subscription
    "aka" Nitro subscription.

    Attributes
    -----------
    NONE:
        Represents no subscription.
    NITRO_CLASSIC:
        Represents a nitro classic subscription.
    NITRO:
        Represents a nitro subscription.
    """
    NONE = 0
    NITRO_CLASSIC = 1
    NITRO = 2

class VerificiationLevel:
    """
    An enumeration that details the verification level of a :class:`Guild`
    that applies to members of that guild.

    Attributes
    -----------
    NONE:
        The guild has no verification level set.
    LOW:
        The member must have verified email on account
    MEDIUM:
        The member must be registered on Discord for longer than 5 minutes
    HIGH:
        The member must be a member of the server for longer than 10 minutes
    VERY_HIGH:
        The member must have a verified phone number on their account.
    """
    NONE = 0
    LOW  = 1
    MEDIUM = 2
    HIGH = 3
    VERY_HIGH = 4

class NotificationLevel:
    """
    An enumeration that details the default notification level of a
    :class:`Guild`.

    Attributes
    -----------
    ALL_MESSAGES:
        The notifications are triggered on every message.
    ONLY_MENTIONS:
        The notifications only trigger on mentions.
    """
    ALL_MESSAGES  = 0
    ONLY_MENTIONS = 1

class ContentFilter:
    """
    An enumeration that details the explicit content filter for a :class:`Guild`.

    Explicit content determines whether the sent content would be scanned for potentially
    explicit content or not.

    Attributes
    -----------
    DISABLED:
        The sent media won't be scanned.
    MEMBER_WITH_ROLES:
        The sent media will only be scanned for members without any roles.
    ALL_MEMBERS:
        The sent media will be scanned for all members.
    """
    DISABLED = 0
    MEMBERS_WITHOUT_ROLES = 1
    ALL_MEMBERS = 2

class MFALevel:
    """
    An enumeration that details the MFA level for moderations actions
    for a :class:`Guild`.

    Attributes
    -----------
    DISABLED:
        There is no 2fa requirement for the guild.
    ELEVATED:
        The moderator must have 2fa enabled to perform moderation actions.
    """
    DISABLED = 0
    ELEVATED = 1

class NSFWLevel:
    """
    An enumeration that details the NSFW level of a :class:`Guild`.

    NSFW level determines whether the guild is marked NSFW or not.

    Attributes
    -----------
    DEFAULT:
        No NSFW level set.
    EXPLICIT:
        The guild is marked explicit.
    SAFE:
        The guild is marked safe for work.
    AGE_RESTRICTED:
        The guild is age restricted.
    """
    DEFAULT  = 0
    EXPLICIT = 1
    SAFE = 2
    AGE_RESTRICTED = 3

class PremiumTier:
    """
    An enumeration that details the premium tier or boost level of a :class:`Guild`.

    Attributes
    -----------
    NONE:
        The guild has no level yet.
    TIER_1:
        The guild has unlocked the tier 1.
    TIER_2:
        The guild has unlocked the tier 2.
    TIER_3:
        The guild has unlocked the tier 3.
    """
    DEFAULT  = 0
    EXPLICIT = 1
    SAFE = 2
    AGE_RESTRICTED = 3