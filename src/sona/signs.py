# Generated from the JSON schema of sona Linku


from typing import Dict, List, Required, TypedDict

Signs = Dict[str, "_SignsAdditionalproperties"]
"""
A raw data object containing information about Luka Pona signs

propertyNames:
  minLength: 1
"""


class _SignsAdditionalproperties(TypedDict, total=False):
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

    etymology: Required[List["_SignsAdditionalpropertiesEtymologyItem"]]
    """
    Unlocalized etymological values regarding this sign's origin

    Required property
    """

    signwriting: Required["_SignsAdditionalpropertiesSignwriting"]
    """
    Scripts for representing a sign as characters.

    Required property
    """

    video: Required["_SignsAdditionalpropertiesVideo"]
    """
    Videos of the sign being performed, by format.

    Required property
    """

    translations: Required[
        Dict[str, "_SignsAdditionalpropertiesTranslationsAdditionalproperties"]
    ]
    """ Required property """


class _SignsAdditionalpropertiesEtymologyItem(TypedDict, total=False):
    language: Required[str]
    """
    The language of the sign.

    Required property
    """

    sign: str
    """ The name of the sign such that it could be found in a sign language dictionary. """


class _SignsAdditionalpropertiesSignwriting(TypedDict, total=False):
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


class _SignsAdditionalpropertiesTranslationsAdditionalproperties(
    TypedDict, total=False
):
    parameters: Required[
        "_SignsAdditionalpropertiesTranslationsAdditionalpropertiesParameters"
    ]
    """ Required property """

    icons: Required[str]
    """ Required property """


class _SignsAdditionalpropertiesTranslationsAdditionalpropertiesParameters(
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


class _SignsAdditionalpropertiesVideo(TypedDict, total=False):
    """Videos of the sign being performed, by format."""

    gif: Required[str]
    """
    A link to a gif of the sign being signed.

    Required property
    """

    mp4: Required[str]
    """
    a link to an mp4 of the sign being signed.

    Required property
    """
