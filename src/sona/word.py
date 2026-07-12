# Generated from the JSON schema of sona Linku


from typing import Literal, Required, TypedDict


class Word(TypedDict, total=False):
    """General info on a Toki Pona word"""

    id: Required["_Schema1"]
    """
    A unique identifier for an object in Linku. Generally named after the object.

    minLength: 1

    Required property
    """

    word: Required["_Schema2"]
    """
    The latin alphabet representation of the word.

    minLength: 1

    Required property
    """

    author_verbatim: str
    author_source: "_Schema6"
    """ The source or origin of this object, often a URL. """

    book: Required["_Schema7"]
    """
    Which official Toki Pona book was this word featured in, if any.

    Required property
    """

    coined_era: Required["_Schema8"]
    """
    The period of time in which this word was coined, relative to the publication of the first two official Toki Pona books

    Required property
    """

    creation_date: Required["_Schema9"]
    """
    When this word was coined, to precision known.

    pattern: ^(?:|(?<year>20\d{2})(?:-(?<month>0[1-9]|1[0-2])(?:-(?<day>0[1-9]|[12]\d|3[01]))?)?|(?<startYear>20\d{2})-(?<endYear>20\d{2}))$

    Required property
    """

    author: Required["_Schema10"]
    """
    The name or names of those involved in creating this word.

    Required property
    """

    ku_data: "_Schema13"
    """
    propertyNames:
      __type__: string
      description: A possible translation of the word into English, as listed in the Toki
        Pona dictionary.
      minLength: 1
    """

    parent_id: "_Schema1"
    """
    A unique identifier for an object in Linku. Generally named after the object.

    minLength: 1
    """

    see_also: Required["_Schema18"]
    """
    The IDs of one or more objects related to this one.

    Required property
    """

    resources: Required["_Schema19"]
    """
    Non-Linku resources related to the specific word, such as wiki links.

    Required property
    """

    representations: Required["_Schema23"]
    """
    Ways of representing this word via text/computers

    Required property
    """

    source_language: Required["_Schema34"]
    """
    The language this word originated from

    minLength: 1

    Required property
    """

    usage_category: Required["_Schema35"]
    """
    The word's usage category, derived from the data of the annual Linku word survey.

    Required property
    """

    deprecated: Required["_Schema36"]
    """
    Whether this word is considered deprecated by its author(s).

    Required property
    """

    audio: Required[list["_Schema37Item"]]
    """ Required property """

    pu_verbatim: "_Schema41"
    usage: Required["_Schema43"]
    """
    The percentage of respondents to the annual Linku word survey who report to use this word, by the date of the survey.

    propertyNames:
      $ref: '#/$defs/__schema44'

    Required property
    """

    glyph_ids: Required["_Schema18"]
    """
    The IDs of one or more objects related to this one.

    Required property
    """

    primary_glyph_id: "_Schema1"
    """
    A unique identifier for an object in Linku. Generally named after the object.

    minLength: 1
    """

    image: "_Schema21"
    """
    A URL pointing to some external resource.

    format: uri
    """

    svg: "_Schema21"
    """
    A URL pointing to some external resource.

    format: uri
    """

    translations: Required["_Schema50"]
    """ Required property """


_Schema1 = str
"""
A unique identifier for an object in Linku. Generally named after the object.

minLength: 1
"""


_Schema10 = list["_Schema11"]
""" The name or names of those involved in creating this word. """


_Schema11 = str
""" minLength: 1 """


_Schema13 = dict[str, "_Schema14"]
"""
propertyNames:
  __type__: string
  description: A possible translation of the word into English, as listed in the Toki
    Pona dictionary.
  minLength: 1
"""


_Schema14 = int | float
"""
minimum: 0
maximum: 100
"""


_Schema18 = list["_Schema1"]
""" The IDs of one or more objects related to this one. """


class _Schema19(TypedDict, total=False):
    """Non-Linku resources related to the specific word, such as wiki links."""

    sona_pona: "_Schema21"
    """
    A URL pointing to some external resource.

    format: uri
    """

    lipamanka_semantic: "_Schema21"
    """
    A URL pointing to some external resource.

    format: uri
    """


_Schema2 = str
"""
The latin alphabet representation of the word.

minLength: 1
"""


_Schema21 = str
"""
A URL pointing to some external resource.

format: uri
"""


class _Schema23(TypedDict, total=False):
    """Ways of representing this word via text/computers"""

    sitelen_emosi: "_Schema25"
    """
    minLength: 1
    format: emoji
    pattern: ^(\p{Extended_Pictographic}|\p{Emoji_Component})+$
    """

    sitelen_jelo: "_Schema27"
    """ minItems: 1 """

    ligatures: list["_Schema30Item"]
    sitelen_sitelen: "_Schema21"
    """
    A URL pointing to some external resource.

    format: uri
    """

    ucsur: "_Schema33"
    """ pattern: ^U\+[\da-fA-F]{4,6}$ """


_Schema25 = str
"""
minLength: 1
format: emoji
pattern: ^(\p{Extended_Pictographic}|\p{Emoji_Component})+$
"""


_Schema27 = list["_Schema28"]
""" minItems: 1 """


_Schema28 = str
"""
minLength: 1
format: emoji
pattern: ^(\p{Extended_Pictographic}|\p{Emoji_Component})+$
"""


_Schema30Item = str
""" minLength: 1 """


_Schema33 = str
""" pattern: ^U\+[\da-fA-F]{4,6}$ """


_Schema34 = str
"""
The language this word originated from

minLength: 1
"""


_Schema35 = (
    Literal["core"]
    | Literal["common"]
    | Literal["uncommon"]
    | Literal["obscure"]
    | Literal["sandbox"]
)
""" The word's usage category, derived from the data of the annual Linku word survey. """
_SCHEMA35_CORE: Literal["core"] = "core"
"""The values for the 'The word's usage category, derived from the data of the annual Linku word survey' enum"""
_SCHEMA35_COMMON: Literal["common"] = "common"
"""The values for the 'The word's usage category, derived from the data of the annual Linku word survey' enum"""
_SCHEMA35_UNCOMMON: Literal["uncommon"] = "uncommon"
"""The values for the 'The word's usage category, derived from the data of the annual Linku word survey' enum"""
_SCHEMA35_OBSCURE: Literal["obscure"] = "obscure"
"""The values for the 'The word's usage category, derived from the data of the annual Linku word survey' enum"""
_SCHEMA35_SANDBOX: Literal["sandbox"] = "sandbox"
"""The values for the 'The word's usage category, derived from the data of the annual Linku word survey' enum"""


_Schema36 = bool
""" Whether this word is considered deprecated by its author(s). """


class _Schema37Item(TypedDict, total=False):
    """Audio files of the words pronounced out loud"""

    author: Required["_Schema11"]
    """
    minLength: 1

    Required property
    """

    link: Required["_Schema21"]
    """
    A URL pointing to some external resource.

    format: uri

    Required property
    """


class _Schema41(TypedDict, total=False):
    en: Required["_Schema42"]
    """
    Localized definition on the parent, such as a word or luka pona sign

    minLength: 1

    Required property
    """

    fr: Required["_Schema42"]
    """
    Localized definition on the parent, such as a word or luka pona sign

    minLength: 1

    Required property
    """

    de: Required["_Schema42"]
    """
    Localized definition on the parent, such as a word or luka pona sign

    minLength: 1

    Required property
    """

    eo: Required["_Schema42"]
    """
    Localized definition on the parent, such as a word or luka pona sign

    minLength: 1

    Required property
    """


_Schema42 = str
"""
Localized definition on the parent, such as a word or luka pona sign

minLength: 1
"""


_Schema43 = dict[str, "_Schema14"]
"""
The percentage of respondents to the annual Linku word survey who report to use this word, by the date of the survey.

propertyNames:
  $ref: '#/$defs/__schema44'
"""


class _Schema50(TypedDict, total=False):
    commentary: Required[str]
    """
    Localized commentary on this word, such as history, clarifications, or trivia.

    Required property
    """

    etymology: Required[str]
    """
    Localized etymology of this word.

    Required property
    """

    definition: Required["_Schema42"]
    """
    Localized definition on the parent, such as a word or luka pona sign

    minLength: 1

    Required property
    """


_Schema6 = str
""" The source or origin of this object, often a URL. """


_Schema7 = Literal["pu"] | Literal["ku suli"] | Literal["ku lili"] | Literal["none"]
""" Which official Toki Pona book was this word featured in, if any. """
_SCHEMA7_PU: Literal["pu"] = "pu"
"""The values for the 'Which official Toki Pona book was this word featured in, if any' enum"""
_SCHEMA7_KU_SULI: Literal["ku suli"] = "ku suli"
"""The values for the 'Which official Toki Pona book was this word featured in, if any' enum"""
_SCHEMA7_KU_LILI: Literal["ku lili"] = "ku lili"
"""The values for the 'Which official Toki Pona book was this word featured in, if any' enum"""
_SCHEMA7_NONE: Literal["none"] = "none"
"""The values for the 'Which official Toki Pona book was this word featured in, if any' enum"""


_Schema8 = Literal["pre-pu"] | Literal["post-pu"] | Literal["post-ku"]
""" The period of time in which this word was coined, relative to the publication of the first two official Toki Pona books """
_SCHEMA8_PRE_PU: Literal["pre-pu"] = "pre-pu"
"""The values for the 'The period of time in which this word was coined, relative to the publication of the first two official Toki Pona books' enum"""
_SCHEMA8_POST_PU: Literal["post-pu"] = "post-pu"
"""The values for the 'The period of time in which this word was coined, relative to the publication of the first two official Toki Pona books' enum"""
_SCHEMA8_POST_KU: Literal["post-ku"] = "post-ku"
"""The values for the 'The period of time in which this word was coined, relative to the publication of the first two official Toki Pona books' enum"""


_Schema9 = str
"""
When this word was coined, to precision known.

pattern: ^(?:|(?<year>20\d{2})(?:-(?<month>0[1-9]|1[0-2])(?:-(?<day>0[1-9]|[12]\d|3[01]))?)?|(?<startYear>20\d{2})-(?<endYear>20\d{2}))$
"""
