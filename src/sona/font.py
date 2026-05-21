# Generated from the JSON schema of sona Linku


from typing import Literal, Required, TypedDict


class Font(TypedDict, total=False):
    """Info on a font for Toki Pona"""

    id: Required["_Schema0"]
    """
    The font's unique ID, identifying it among other fonts

    minLength: 1

    Required property
    """

    author: Required["_Schema1"]
    """
    a list of this font's authors

    Required property
    """

    features: Required["_Schema3"]
    """
    a list of features this font supports

    Required property
    """

    filename: Required["_Schema5"]
    """
    the name of the file this font is stored in at https://github.com/lipu-linku/ijo

    pattern: ^(?:.+\.(ttf|otf|woff2|woff))?$

    Required property
    """

    last_updated: Required["_Schema6"]
    """
    the rough date of this font's last update

    pattern: ^(?:|(?<year>20\d{2})(?:-(?<month>0[1-9]|1[0-2])(?:-(?<day>0[1-9]|[12]\d|3[01]))?)?|(?<startYear>20\d{2})-(?<endYear>20\d{2}))$

    Required property
    """

    license: Required["_Schema7"]
    """
    an SPDX expression describing this font's license: https://spdx.org/licenses/

    Required property
    """

    ligatures: Required["_Schema8"]
    """
    whether this font supports ligatures

    Required property
    """

    name: Required["_Schema9"]
    """
    this font's name

    minLength: 1

    Required property
    """

    style: Required["_Schema10"]
    """
    the general style of this font

    minLength: 1

    Required property
    """

    ucsur: Required["_Schema11"]
    """
    whether this font conforms to the UCSUR standard: https://www.kreativekorp.com/ucsur/charts/sitelen.html

    Required property
    """

    version: Required["_Schema12"]
    """
    the current version of this font

    Required property
    """

    writing_system: Required["_Schema13"]
    """
    the writing system this font uses as its script

    Required property
    """

    links: Required["_Schema14"]
    """ Required property """


_Schema0 = str
"""
The font's unique ID, identifying it among other fonts

minLength: 1
"""


_Schema1 = list["_Schema2"]
""" a list of this font's authors """


_Schema10 = str
"""
the general style of this font

minLength: 1
"""


_Schema11 = bool
""" whether this font conforms to the UCSUR standard: https://www.kreativekorp.com/ucsur/charts/sitelen.html """


_Schema12 = str
""" the current version of this font """


_Schema13 = (
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
_SCHEMA13_SITELEN_PONA: Literal["sitelen pona"] = "sitelen pona"
"""The values for the 'the writing system this font uses as its script' enum"""
_SCHEMA13_SITELEN_SITELEN: Literal["sitelen sitelen"] = "sitelen sitelen"
"""The values for the 'the writing system this font uses as its script' enum"""
_SCHEMA13_ALPHABET: Literal["alphabet"] = "alphabet"
"""The values for the 'the writing system this font uses as its script' enum"""
_SCHEMA13_SYLLABARY: Literal["syllabary"] = "syllabary"
"""The values for the 'the writing system this font uses as its script' enum"""
_SCHEMA13_LOGOGRAPHY: Literal["logography"] = "logography"
"""The values for the 'the writing system this font uses as its script' enum"""
_SCHEMA13_TOKIPONIDO_ALPHABET: Literal["tokiponido alphabet"] = "tokiponido alphabet"
"""The values for the 'the writing system this font uses as its script' enum"""
_SCHEMA13_TOKIPONIDO_SYLLABARY: Literal["tokiponido syllabary"] = "tokiponido syllabary"
"""The values for the 'the writing system this font uses as its script' enum"""
_SCHEMA13_TOKIPONIDO_LOGOGRAPHY: Literal["tokiponido logography"] = (
    "tokiponido logography"
)
"""The values for the 'the writing system this font uses as its script' enum"""


class _Schema14(TypedDict, total=False):
    fontfile: "_Schema15"
    """
    A URL pointing to some external resource.

    format: uri
    """

    repo: "_Schema15"
    """
    A URL pointing to some external resource.

    format: uri
    """

    webpage: "_Schema15"
    """
    A URL pointing to some external resource.

    format: uri
    """


_Schema15 = str
"""
A URL pointing to some external resource.

format: uri
"""


_Schema2 = str
""" minLength: 1 """


_Schema3 = list["_Schema4"]
""" a list of features this font supports """


_Schema4 = str
""" minLength: 1 """


_Schema5 = str
"""
the name of the file this font is stored in at https://github.com/lipu-linku/ijo

pattern: ^(?:.+\.(ttf|otf|woff2|woff))?$
"""


_Schema6 = str
"""
the rough date of this font's last update

pattern: ^(?:|(?<year>20\d{2})(?:-(?<month>0[1-9]|1[0-2])(?:-(?<day>0[1-9]|[12]\d|3[01]))?)?|(?<startYear>20\d{2})-(?<endYear>20\d{2}))$
"""


_Schema7 = str
""" an SPDX expression describing this font's license: https://spdx.org/licenses/ """


_Schema8 = bool
""" whether this font supports ligatures """


_Schema9 = str
"""
this font's name

minLength: 1
"""
