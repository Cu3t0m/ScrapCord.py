.. currentmodule:: scrapcord

API Reference
===============

This API reference marks every aspect of this library.

Version Related Info
---------------------

.. data:: __version__

    A string representation of the version. e.g. ``'1.0.0rc1'``. This is based
    off of :pep:`440`.

Clients
--------

Client
~~~~~~~

.. autoclass:: Client
    :members:


Enumerations
-------------

Discord API provides integers based enumerations for precision and consistency purposes.
These classes provides named attributes to access those enumerations.

PremiumType
~~~~~~~~~~~~~

.. autoclass:: PremiumType
    :members:

VerificationLevel
~~~~~~~~~~~~~~~~~~~

.. autoclass:: VerificationLevel
    :members:


NotificationLevel
~~~~~~~~~~~~~~~~~~~

.. autoclass:: NotificationLevel
    :members:

ContentFilter
~~~~~~~~~~~~~~~~~~~

.. autoclass:: ContentFilter
    :members:

MFALevel
~~~~~~~~~~~~~

.. autoclass:: MFALevel
    :members:


NSFWLevel
~~~~~~~~~~~~~

.. autoclass:: NSFWLevel
    :members:

PremiumTier
~~~~~~~~~~~~~

.. autoclass:: PremiumTier
    :members:


Abstract Base Classes
---------------------

Abstract Base Classes are the base classes that implement common operations for certain
classes. This library also implements some ABCs.

Please note that these ABCs are not meant to be used in general and are exposed
for documentation purposes only.

DiscordModel
~~~~~~~~~~~~

.. autoclass:: aiocord.abc.DiscordModel
    :members:

Discord Data Models
--------------------

These classes wrap the data sent by Discord in easy to use OOP-based form. Since these classes
are often cached internally, So for performance purposes, All of these classes have
``__slots__`` set which prevents dynamic attributes on this classes.

Do not create these classes manually or modify the internal cache as it might result in
your bot's cache getting unsynced and potentially would lead to complicated problems.

User
~~~~~~~

.. autoclass:: User
    :members:
    :inherited-members:


ClientUser
~~~~~~~~~~~

.. autoclass:: ClientUser
    :members:
    :inherited-members:

CDNAsset
~~~~~~~~

.. autoclass:: CDNAsset
    :members:

Guild
~~~~~~

.. autoclass:: Guild
    :members:

Flags
-------

GatewayIntents
~~~~~~~~~~~~~~~

.. autoclass:: GatewayIntents
    :members:
    :inherited-members:

UserFlags
~~~~~~~~~~

.. autoclass:: UserFlags
    :members:
    :inherited-members:

Data Classes
------------

Colour
~~~~~~~

.. autoclass:: Colour
    :members: