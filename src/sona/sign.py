# Generated from the JSON schema of sona Linku


from typing import Required, TypedDict


class Sign(TypedDict, total=False):
    """Info on a Luka Pona sign"""

    id: Required["_Schema0"]
    """
    A unique name for the fingerspelling which is also a gloss.

    minLength: 1

    Required property
    """

    is_two_handed: Required["_Schema1"]
    """
    Whether the sign is two-handed or not.

    Required property
    """

    etymology: Required["_Schema2"]
    """
    Unlocalized etymological values regarding this sign's origin

    Required property
    """

    signwriting: Required["_Schema5"]
    """
    Scripts for representing a sign as characters.

    Required property
    """

    video: "_Schema8"
    """ Videos of the sign being performed, by format. """

    translations: Required["_Schema12"]
    """ Required property """

    definition: Required["_Schema21"]
    """
    The definition of the sign as a single toki pona word.

    Required property
    """

    new_gloss: Required["_Schema22"]
    """
    The more recent, preferred gloss for this sign.

    Required property
    """

    old_gloss: Required["_Schema23"]
    """
    The older gloss for this sign, similar to `id`.

    Required property
    """

    old_id: Required["_Schema24"]
    """
    Previous, malformed id for the sign.

    Required property
    """


_Schema0 = str
"""
A unique name for the fingerspelling which is also a gloss.

minLength: 1
"""


_Schema1 = bool
""" Whether the sign is two-handed or not. """


_Schema10 = str
"""
A URL pointing to some external resource.

format: uri
"""


class _Schema12(TypedDict, total=False):
    icons: Required[str]
    """
    Localized descriptions of the thing a sign represents.

    Required property
    """

    parameters: Required["_Schema12Parameters"]
    """
    Partly localized descriptions of how a sign is signed.

    Required property
    """


class _Schema12Parameters(TypedDict, total=False):
    """Partly localized descriptions of how a sign is signed."""

    handshape: str
    movement: str
    placement: str
    orientation: str


_Schema2 = list["_Schema3"]
""" Unlocalized etymological values regarding this sign's origin """


_Schema21 = str
""" The definition of the sign as a single toki pona word. """


_Schema22 = str
""" The more recent, preferred gloss for this sign. """


_Schema23 = str
""" The older gloss for this sign, similar to `id`. """


_Schema24 = str
""" Previous, malformed id for the sign. """


class _Schema3(TypedDict, total=False):
    language: Required[str]
    """
    The language of the sign.

    Required property
    """

    sign: str


class _Schema5(TypedDict, total=False):
    """Scripts for representing a sign as characters."""

    fsw: Required["_Schema6"]
    """
    The [Formal SignWriting](https://en.wikipedia.org/wiki/SignWriting) representation of the sign.

    minLength: 1

    Required property
    """

    swu: Required["_Schema7"]
    """
    The [SignWriting with Unicode](https://en.wikipedia.org/wiki/SignWriting) representation of the sign.

    minLength: 1

    Required property
    """


_Schema6 = str
"""
The [Formal SignWriting](https://en.wikipedia.org/wiki/SignWriting) representation of the sign.

minLength: 1
"""


_Schema7 = str
"""
The [SignWriting with Unicode](https://en.wikipedia.org/wiki/SignWriting) representation of the sign.

minLength: 1
"""


class _Schema8(TypedDict, total=False):
    """Videos of the sign being performed, by format."""

    gif: Required["_Schema10"]
    """
    A URL pointing to some external resource.

    format: uri

    Required property
    """

    mp4: Required["_Schema10"]
    """
    A URL pointing to some external resource.

    format: uri

    Required property
    """
