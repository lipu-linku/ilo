# Generated from the JSON schema of sona Linku


from typing import Literal, Required, TypedDict

Fonts = dict[str, "_Schema1"]
"""
A raw data object containing all fonts data in Linku

propertyNames:
  $ref: '#/$defs/__schema0'
"""


_Schema0 = str
"""
A unique identifier for an object in Linku. Generally named after the object.

minLength: 1
"""


class _Schema1(TypedDict, total=False):
    """Info on a font for Toki Pona"""

    id: Required["_Schema0"]
    """
    A unique identifier for an object in Linku. Generally named after the object.

    minLength: 1

    Required property
    """

    author: Required["_Schema3"]
    """
    a list of this font's authors

    Required property
    """

    features: Required["_Schema5"]
    """
    a list of features this font supports

    Required property
    """

    filename: Required["_Schema7"]
    """
    the name of the file this font is stored in at https://github.com/lipu-linku/ijo

    pattern: ^(?:.+\.(ttf|otf|woff2|woff))?$

    Required property
    """

    last_updated: Required["_Schema8"]
    """
    the rough date of this font's last update

    pattern: ^(?:|(?<year>20\d{2})(?:-(?<month>0[1-9]|1[0-2])(?:-(?<day>0[1-9]|[12]\d|3[01]))?)?|(?<startYear>20\d{2})-(?<endYear>20\d{2}))$

    Required property
    """

    license: Required["_Schema9"]
    """
    an SPDX expression describing this font's license: https://spdx.org/licenses/

    Required property
    """

    ligatures: Required["_Schema10"]
    """
    whether this font supports ligatures

    Required property
    """

    name: Required["_Schema11"]
    """
    this font's name

    minLength: 1

    Required property
    """

    style: Required["_Schema12"]
    """
    the general style of this font

    minLength: 1

    Required property
    """

    ucsur: Required["_Schema13"]
    """
    whether this font conforms to the UCSUR standard: https://www.kreativekorp.com/ucsur/charts/sitelen.html

    Required property
    """

    version: Required["_Schema14"]
    """
    the current version of this font

    Required property
    """

    writing_system: Required["_Schema15"]
    """
    the writing system this font uses as its script

    Required property
    """

    links: Required["_Schema16"]
    """ Required property """


_Schema10 = bool
""" whether this font supports ligatures """


_Schema11 = str
"""
this font's name

minLength: 1
"""


_Schema12 = str
"""
the general style of this font

minLength: 1
"""


_Schema13 = bool
""" whether this font conforms to the UCSUR standard: https://www.kreativekorp.com/ucsur/charts/sitelen.html """


_Schema14 = str
""" the current version of this font """


_Schema15 = (
    Literal["sitelen pona"]
    | Literal["sitelen sitelen"]
    | Literal["alphabet"]
    | Literal["syllabary"]
    | Literal["logography"]
    | Literal["tokiponido alphabet"]
    | Literal["tokiponido syllabary"]
    | Literal["tokiponido logography"]
)
""" the writing system this font uses as its script """
_SCHEMA15_SITELEN_PONA: Literal["sitelen pona"] = "sitelen pona"
"""The values for the 'the writing system this font uses as its script' enum"""
_SCHEMA15_SITELEN_SITELEN: Literal["sitelen sitelen"] = "sitelen sitelen"
"""The values for the 'the writing system this font uses as its script' enum"""
_SCHEMA15_ALPHABET: Literal["alphabet"] = "alphabet"
"""The values for the 'the writing system this font uses as its script' enum"""
_SCHEMA15_SYLLABARY: Literal["syllabary"] = "syllabary"
"""The values for the 'the writing system this font uses as its script' enum"""
_SCHEMA15_LOGOGRAPHY: Literal["logography"] = "logography"
"""The values for the 'the writing system this font uses as its script' enum"""
_SCHEMA15_TOKIPONIDO_ALPHABET: Literal["tokiponido alphabet"] = "tokiponido alphabet"
"""The values for the 'the writing system this font uses as its script' enum"""
_SCHEMA15_TOKIPONIDO_SYLLABARY: Literal["tokiponido syllabary"] = "tokiponido syllabary"
"""The values for the 'the writing system this font uses as its script' enum"""
_SCHEMA15_TOKIPONIDO_LOGOGRAPHY: Literal["tokiponido logography"] = (
    "tokiponido logography"
)
"""The values for the 'the writing system this font uses as its script' enum"""


class _Schema16(TypedDict, total=False):
    fontfile: "_Schema17"
    """
    A URL pointing to some external resource.

    format: uri
    """

    repo: "_Schema17"
    """
    A URL pointing to some external resource.

    format: uri
    """

    webpage: "_Schema17"
    """
    A URL pointing to some external resource.

    format: uri
    """


_Schema17 = str
"""
A URL pointing to some external resource.

format: uri
"""


_Schema3 = list["_Schema4"]
""" a list of this font's authors """


_Schema4 = str
""" minLength: 1 """


_Schema5 = list["_Schema6"]
""" a list of features this font supports """


_Schema6 = str
""" minLength: 1 """


_Schema7 = str
"""
the name of the file this font is stored in at https://github.com/lipu-linku/ijo

pattern: ^(?:.+\.(ttf|otf|woff2|woff))?$
"""


_Schema8 = str
"""
the rough date of this font's last update

pattern: ^(?:|(?<year>20\d{2})(?:-(?<month>0[1-9]|1[0-2])(?:-(?<day>0[1-9]|[12]\d|3[01]))?)?|(?<startYear>20\d{2})-(?<endYear>20\d{2}))$
"""


_Schema9 = str
""" an SPDX expression describing this font's license: https://spdx.org/licenses/ """
