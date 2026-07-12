# Generated from the JSON schema of sona Linku


from typing import Literal, Required, TypedDict


class Glyph(TypedDict, total=False):
    id: Required["_Schema0"]
    """
    A unique identifier for an object in Linku. Generally named after the object.

    minLength: 1

    Required property
    """

    word: Required[str]
    """
    The toki pona word which is written with this glyph.

    minLength: 1

    Required property
    """

    word_id: Required["_Schema0"]
    """
    A unique identifier for an object in Linku. Generally named after the object.

    minLength: 1

    Required property
    """

    usage_category: Required["_GlyphUsageCategory"]
    """
    The glyph's usage category, derived from the data of the annual Linku glyph survey.

    Required property
    """

    author: Required[list["_Schema1"]]
    """
    The name or names of those involved in creating this glyph.

    Required property
    """

    author_source: "_Schema2"
    """ The source or origin of this object, often a URL. """

    creation_date: Required[str]
    """
    When this glyph was created, to precision known

    pattern: ^(?:|(?<year>20\d{2})(?:-(?<month>0[1-9]|1[0-2])(?:-(?<day>0[1-9]|[12]\d|3[01]))?)?|(?<startYear>20\d{2})-(?<endYear>20\d{2}))$

    Required property
    """

    see_also: Required[list["_Schema0"]]
    """
    A list of related glyphs by ID

    Required property
    """

    primary: Required[bool]
    """
    Whether this glyph is the main glyph used to write the toki pona word in `word`

    Required property
    """

    parent_id: "_Schema0"
    """
    A unique identifier for an object in Linku. Generally named after the object.

    minLength: 1
    """

    deprecated: Required[bool]
    """
    Whether this glyph is considered deprecated by its author(s).

    Required property
    """

    image: "_Schema4"
    """
    A URL pointing to some external resource.

    format: uri
    """

    svg: "_Schema4"
    """
    A URL pointing to some external resource.

    format: uri
    """

    ligature: "_Schema5"
    """ minLength: 1 """

    alias_ligatures: list["_Schema5"]
    ucsur: "_Schema7"
    """ pattern: ^U\+[\da-fA-F]{4,6}$ """

    usage: Required[dict[str, "_Schema9"]]
    """
    The percentage of respondents to the annual Linku word survey who report to use this glyph, by the date of the survey.

    propertyNames:
      $ref: '#/$defs/__schema8'

    Required property
    """

    translations: Required["_GlyphTranslations"]
    """ Required property """


class _GlyphTranslations(TypedDict, total=False):
    commentary: Required[str]
    """
    Localized commentary on this glyph, such as history, clarifications, or trivia.

    Required property
    """

    etymology: Required[str]
    """
    Localized etymology of this glyph.

    Required property
    """

    names: Required[list["_Schema10"]]
    """
    A list of names used to refer to this sitelen pona glyph

    Required property
    """


_GlyphUsageCategory = (
    Literal["core"]
    | Literal["common"]
    | Literal["uncommon"]
    | Literal["obscure"]
    | Literal["sandbox"]
)
""" The glyph's usage category, derived from the data of the annual Linku glyph survey. """
_GLYPHUSAGECATEGORY_CORE: Literal["core"] = "core"
"""The values for the 'The glyph's usage category, derived from the data of the annual Linku glyph survey' enum"""
_GLYPHUSAGECATEGORY_COMMON: Literal["common"] = "common"
"""The values for the 'The glyph's usage category, derived from the data of the annual Linku glyph survey' enum"""
_GLYPHUSAGECATEGORY_UNCOMMON: Literal["uncommon"] = "uncommon"
"""The values for the 'The glyph's usage category, derived from the data of the annual Linku glyph survey' enum"""
_GLYPHUSAGECATEGORY_OBSCURE: Literal["obscure"] = "obscure"
"""The values for the 'The glyph's usage category, derived from the data of the annual Linku glyph survey' enum"""
_GLYPHUSAGECATEGORY_SANDBOX: Literal["sandbox"] = "sandbox"
"""The values for the 'The glyph's usage category, derived from the data of the annual Linku glyph survey' enum"""


_Schema0 = str
"""
A unique identifier for an object in Linku. Generally named after the object.

minLength: 1
"""


_Schema1 = str
""" minLength: 1 """


_Schema10 = str
""" A name this sitelen pona glyph is known by. """


_Schema2 = str
""" The source or origin of this object, often a URL. """


_Schema4 = str
"""
A URL pointing to some external resource.

format: uri
"""


_Schema5 = str
""" minLength: 1 """


_Schema7 = str
""" pattern: ^U\+[\da-fA-F]{4,6}$ """


_Schema9 = int | float
"""
minimum: 0
maximum: 100
"""
