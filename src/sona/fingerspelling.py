# Generated from the JSON schema of sona Linku


from typing import Dict, List, Required, TypedDict

Fingerspelling = Dict[str, "_FingerspellingAdditionalproperties"]
"""
A raw data object containing information about Luka Pona fingerspelling signs

propertyNames:
  minLength: 1
"""


class _FingerspellingAdditionalproperties(TypedDict, total=False):
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

    etymology: Required[List["_FingerspellingAdditionalpropertiesEtymologyItem"]]
    """
    Unlocalized etymological values regarding this sign's origin

    Required property
    """

    signwriting: Required["_FingerspellingAdditionalpropertiesSignwriting"]
    """
    Scripts for representing a sign as characters.

    Required property
    """

    video: Required["_FingerspellingAdditionalpropertiesVideo"]
    """
    Videos of the sign being performed, by format.

    Required property
    """

    translations: Required[
        Dict[str, "_FingerspellingAdditionalpropertiesTranslationsAdditionalproperties"]
    ]
    """ Required property """


class _FingerspellingAdditionalpropertiesEtymologyItem(TypedDict, total=False):
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


class _FingerspellingAdditionalpropertiesSignwriting(TypedDict, total=False):
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


class _FingerspellingAdditionalpropertiesTranslationsAdditionalproperties(
    TypedDict, total=False
):
    parameters: Required[
        "_FingerspellingAdditionalpropertiesTranslationsAdditionalpropertiesParameters"
    ]
    """ Required property """


class _FingerspellingAdditionalpropertiesTranslationsAdditionalpropertiesParameters(
    TypedDict, total=False
):
    handshape: str
    """ The shape of the hand when signing, identified by its name in ASL. Should not be translated in any language other than Toki Pona """

    movement: str
    """ The motion of the hand when signing. """

    placement: str
    """ The placement of the hand when signing. """

    orientation: str
    """ The orientation of the hand when signing. """


class _FingerspellingAdditionalpropertiesVideo(TypedDict, total=False):
    """Videos of the sign being performed, by format."""

    gif: str
    """ A link to a gif of the sign being signed. """

    mp4: str
    """ a link to an mp4 of the sign being signed. """
