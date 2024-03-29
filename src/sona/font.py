# Generated from the JSON schema of sona Linku


from typing import List, Literal, Required, TypedDict, Union


class Font(TypedDict, total=False):
    """Info on a font for Toki Pona"""

    id: Required[str]
    """
    The font's unique ID, identifying it among other fonts

    minLength: 1

    Required property
    """

    creator: Required[List[str]]
    """
    a list of this font's creators

    Required property
    """

    features: Required[List[str]]
    """
    a list of features this font supports

    Required property
    """

    filename: Required[str]
    """
    the name of the file this font is stored in at https://github.com/lipu-linku/ijo

    pattern: ^(?:.+\.(ttf|otf|woff2|woff))?$

    Required property
    """

    last_updated: str
    """
    the rough date of this font's last update

    pattern: ^20\d{2}-(0[1-9]|1[0-2])$
    """

    license: Required[str]
    """
    an SPDX expression describing this font's license: https://spdx.org/licenses/

    Required property
    """

    ligatures: Required[bool]
    """
    whether this font supports ligatures

    Required property
    """

    name: Required[str]
    """
    this font's name

    minLength: 1

    Required property
    """

    style: Required[str]
    """
    the general style of this font

    minLength: 1

    Required property
    """

    ucsur: Required[bool]
    """
    whether this font conforms to the UCSUR standard: https://www.kreativekorp.com/ucsur/charts/sitelen.html

    Required property
    """

    version: Required[str]
    """
    the current version of this font

    Required property
    """

    writing_system: Required["_FontWritingSystem"]
    """
    the writing system this font uses as its script

    Required property
    """

    links: Required["_FontLinks"]
    """ Required property """


class _FontLinks(TypedDict, total=False):
    fontfile: str
    """
    a link to the font file published by the original author (not the mirror on the Linku Project's GitHub)

    format: uri
    """

    repo: str
    """
    a link to a web hosted repository of this font's source files (usually hosted on GitHub or GitLab)

    format: uri
    """

    webpage: str
    """
    a link to this font's home page, usually showcasing its features and usage/installation

    format: uri
    """


_FontWritingSystem = Union[
    Literal["sitelen pona"],
    Literal["sitelen sitelen"],
    Literal["alphabet"],
    Literal["syllabary"],
    Literal["logography"],
    Literal["tokiponido alphabet"],
    Literal["tokiponido syllabary"],
    Literal["tokiponido logography"],
]
""" the writing system this font uses as its script """
_FONTWRITINGSYSTEM_SITELEN_PONA: Literal["sitelen pona"] = "sitelen pona"
"""The values for the 'the writing system this font uses as its script' enum"""
_FONTWRITINGSYSTEM_SITELEN_SITELEN: Literal["sitelen sitelen"] = "sitelen sitelen"
"""The values for the 'the writing system this font uses as its script' enum"""
_FONTWRITINGSYSTEM_ALPHABET: Literal["alphabet"] = "alphabet"
"""The values for the 'the writing system this font uses as its script' enum"""
_FONTWRITINGSYSTEM_SYLLABARY: Literal["syllabary"] = "syllabary"
"""The values for the 'the writing system this font uses as its script' enum"""
_FONTWRITINGSYSTEM_LOGOGRAPHY: Literal["logography"] = "logography"
"""The values for the 'the writing system this font uses as its script' enum"""
_FONTWRITINGSYSTEM_TOKIPONIDO_ALPHABET: Literal["tokiponido alphabet"] = (
    "tokiponido alphabet"
)
"""The values for the 'the writing system this font uses as its script' enum"""
_FONTWRITINGSYSTEM_TOKIPONIDO_SYLLABARY: Literal["tokiponido syllabary"] = (
    "tokiponido syllabary"
)
"""The values for the 'the writing system this font uses as its script' enum"""
_FONTWRITINGSYSTEM_TOKIPONIDO_LOGOGRAPHY: Literal["tokiponido logography"] = (
    "tokiponido logography"
)
"""The values for the 'the writing system this font uses as its script' enum"""
