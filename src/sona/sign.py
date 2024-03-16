# Generated from the JSON schema of sona Linku


from typing import List, Required, TypedDict


class Sign(TypedDict, total=False):
    """Unlocalized info on a Luka Pona sign"""

    definition: Required[str]
    """
    The definition of the sign as a single toki pona word.

    Required property
    """

    id: Required[str]
    """
    A globally unique name for the sign which is also a gloss.

    Required property
    """

    is_two_handed: Required[bool]
    """
    Whether the sign is two-handed or not.

    Required property
    """

    new_gloss: Required[str]
    """
    The more recent, preferred gloss for this sign.

    Required property
    """

    old_gloss: Required[str]
    """
    The older gloss for this sign, similar to `id`.

    Required property
    """

    etymology: Required[List["_SignEtymologyItem"]]
    """
    Unlocalized etymological values regarding this sign's origin

    Required property
    """

    signwriting: Required["_SignSignwriting"]
    """
    Scripts for representing a sign as characters.

    Required property
    """

    video: Required["_SignVideo"]
    """
    Videos of the sign being performed, by format.

    Required property
    """


class _SignEtymologyItem(TypedDict, total=False):
    language: Required[str]
    """
    The language of the sign.

    Required property
    """

    sign: str
    """ The name of the sign such that it could be found in a sign language dictionary. """


class _SignSignwriting(TypedDict, total=False):
    """Scripts for representing a sign as characters."""

    fsw: Required[str]
    """
    The [Formal SignWriting](https://en.wikipedia.org/wiki/SignWriting) representation of the sign.

    Required property
    """

    swu: Required[str]
    """
    The [SignWriting with Unicode](https://en.wikipedia.org/wiki/SignWriting) representation of the sign.

    Required property
    """


class _SignVideo(TypedDict, total=False):
    """Videos of the sign being performed, by format."""

    gif: str
    """ A link to a gif of the sign being signed. """

    mp4: str
    """ a link to an mp4 of the sign being signed. """
