# Generated from the JSON schema of sona Linku


from typing import List, Required, TypedDict


class FingerspellingSign(TypedDict, total=False):
    """Unlocalized info on a fingerspelling sign."""

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

    etymology: Required[List["_FingerspellingsignEtymologyItem"]]
    """
    Unlocalized etymological values regarding this sign's origin

    Required property
    """

    signwriting: Required["_FingerspellingsignSignwriting"]
    """
    Scripts for representing a sign as characters.

    Required property
    """

    video: Required["_FingerspellingsignVideo"]
    """
    Videos of the sign being performed, by format.

    Required property
    """


class _FingerspellingsignEtymologyItem(TypedDict, total=False):
    language: Required[str]
    """
    The language of the sign.

    Required property
    """

    sign: Required[str]
    """
    The name of the sign such that it could be found in a sign language dictionary.

    Required property
    """


class _FingerspellingsignSignwriting(TypedDict, total=False):
    """Scripts for representing a sign as characters."""

    fsw: Required[str]
    """
    The Formal Sign Writing representation of the sign.

    Required property
    """

    swu: Required[str]
    """
    The Sign Writing with Unicode representation of hte sign.

    Required property
    """


class _FingerspellingsignVideo(TypedDict, total=False):
    """Videos of the sign being performed, by format."""

    gif: str
    """ A link to a gif of the sign being signed. """

    mp4: str
    """ a link to an mp4 of the sign being signed. """
