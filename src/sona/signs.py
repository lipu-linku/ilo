# Generated from the JSON schema of sona Linku


from typing import Required, TypedDict

Signs = dict[str, "_Schema1"]
"""
A raw data object containing information about Luka Pona signs

propertyNames:
  $ref: '#/$defs/__schema0'
"""


_Schema0 = str
"""
A unique identifier for an object in Linku. Generally named after the object.

minLength: 1
"""


class _Schema1(TypedDict, total=False):
    """Info on a Luka Pona sign"""

    id: Required["_Schema0"]
    """
    A unique identifier for an object in Linku. Generally named after the object.

    minLength: 1

    Required property
    """

    is_two_handed: Required["_Schema3"]
    """
    Whether the sign is two-handed or not.

    Required property
    """

    etymology: Required["_Schema4"]
    """
    Unlocalized etymological values regarding this sign's origin

    Required property
    """

    signwriting: Required["_Schema7"]
    """
    Scripts for representing a sign as characters.

    Required property
    """

    video: "_Schema10"
    """ Videos of the sign being performed, by format. """

    translations: Required["_Schema14"]
    """ Required property """

    definition: Required["_Schema23"]
    """
    The definition of the sign as a single toki pona word.

    Required property
    """

    new_gloss: Required["_Schema24"]
    """
    The more recent, preferred gloss for this sign.

    Required property
    """

    old_gloss: Required["_Schema25"]
    """
    The older gloss for this sign, similar to `id`.

    Required property
    """

    old_id: Required["_Schema26"]
    """
    Previous, malformed id for the sign.

    Required property
    """


class _Schema10(TypedDict, total=False):
    """Videos of the sign being performed, by format."""

    gif: Required["_Schema12"]
    """
    A URL pointing to some external resource.

    format: uri

    Required property
    """

    mp4: Required["_Schema12"]
    """
    A URL pointing to some external resource.

    format: uri

    Required property
    """


_Schema12 = str
"""
A URL pointing to some external resource.

format: uri
"""


class _Schema14(TypedDict, total=False):
    icons: Required[str]
    """
    Localized descriptions of the thing a sign represents.

    Required property
    """

    parameters: Required["_Schema14Parameters"]
    """
    Partly localized descriptions of how a sign is signed.

    Required property
    """


class _Schema14Parameters(TypedDict, total=False):
    """Partly localized descriptions of how a sign is signed."""

    handshape: str
    movement: str
    placement: str
    orientation: str


_Schema23 = str
""" The definition of the sign as a single toki pona word. """


_Schema24 = str
""" The more recent, preferred gloss for this sign. """


_Schema25 = str
""" The older gloss for this sign, similar to `id`. """


_Schema26 = str
""" Previous, malformed id for the sign. """


_Schema3 = bool
""" Whether the sign is two-handed or not. """


_Schema4 = list["_Schema5"]
""" Unlocalized etymological values regarding this sign's origin """


class _Schema5(TypedDict, total=False):
    language: Required[str]
    """
    The language of the sign.

    Required property
    """

    sign: str


class _Schema7(TypedDict, total=False):
    """Scripts for representing a sign as characters."""

    fsw: Required["_Schema8"]
    """
    The [Formal SignWriting](https://en.wikipedia.org/wiki/SignWriting) representation of the sign.

    minLength: 1

    Required property
    """

    swu: Required["_Schema9"]
    """
    The [SignWriting with Unicode](https://en.wikipedia.org/wiki/SignWriting) representation of the sign.

    minLength: 1

    Required property
    """


_Schema8 = str
"""
The [Formal SignWriting](https://en.wikipedia.org/wiki/SignWriting) representation of the sign.

minLength: 1
"""


_Schema9 = str
"""
The [SignWriting with Unicode](https://en.wikipedia.org/wiki/SignWriting) representation of the sign.

minLength: 1
"""
