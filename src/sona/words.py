# Generated from the JSON schema of sona Linku


from typing import Literal, Required, TypedDict

Words = dict[str, "_Schema1"]
"""
A raw data object containing dictionary info about Toki Pona words

propertyNames:
  $ref: '#/$defs/__schema0'
"""


_Schema0 = str
"""
A unique identifier for an object in Linku. Generally named after the object.

minLength: 1
"""


class _Schema1(TypedDict, total=False):
    """General info on a Toki Pona word"""

    id: Required["_Schema0"]
    """
    A unique identifier for an object in Linku. Generally named after the object.

    minLength: 1

    Required property
    """

    word: Required["_Schema3"]
    """
    The latin alphabet representation of the word.

    minLength: 1

    Required property
    """

    author_verbatim: str
    author_source: "_Schema7"
    """ The source or origin of this object, often a URL. """

    book: Required["_Schema8"]
    """
    Which official Toki Pona book was this word featured in, if any.

    Required property
    """

    coined_era: Required["_Schema9"]
    """
    The period of time in which this word was coined, relative to the publication of the first two official Toki Pona books

    Required property
    """

    creation_date: Required["_Schema10"]
    """
    When this word was coined, to precision known.

    pattern: ^(?:|(?<year>20\d{2})(?:-(?<month>0[1-9]|1[0-2])(?:-(?<day>0[1-9]|[12]\d|3[01]))?)?|(?<startYear>20\d{2})-(?<endYear>20\d{2}))$

    Required property
    """

    author: Required["_Schema11"]
    """
    The name or names of those involved in creating this word.

    Required property
    """

    ku_data: "_Schema14"
    """
    propertyNames:
      __type__: string
      description: A possible translation of the word into English, as listed in the Toki
        Pona dictionary.
      minLength: 1
    """

    parent_id: "_Schema0"
    """
    A unique identifier for an object in Linku. Generally named after the object.

    minLength: 1
    """

    see_also: Required["_Schema19"]
    """
    The IDs of one or more objects related to this one.

    Required property
    """

    resources: Required["_Schema20"]
    """
    Non-Linku resources related to the specific word, such as wiki links.

    Required property
    """

    representations: Required["_Schema24"]
    """
    Ways of representing this word via text/computers

    Required property
    """

    source_language: Required["_Schema35"]
    """
    The language this word originated from

    minLength: 1

    Required property
    """

    usage_category: Required["_Schema36"]
    """
    The word's usage category, derived from the data of the annual Linku word survey.

    Required property
    """

    deprecated: Required["_Schema37"]
    """
    Whether this word is considered deprecated by its author(s).

    Required property
    """

    audio: Required[list["_Schema38Item"]]
    """ Required property """

    pu_verbatim: "_Schema42"
    usage: Required["_Schema44"]
    """
    The percentage of respondents to the annual Linku word survey who report to use this word, by the date of the survey.

    propertyNames:
      $ref: '#/$defs/__schema45'

    Required property
    """

    glyph_ids: Required["_Schema19"]
    """
    The IDs of one or more objects related to this one.

    Required property
    """

    primary_glyph_id: "_Schema0"
    """
    A unique identifier for an object in Linku. Generally named after the object.

    minLength: 1
    """

    image: "_Schema22"
    """
    A URL pointing to some external resource.

    format: uri
    """

    svg: "_Schema22"
    """
    A URL pointing to some external resource.

    format: uri
    """

    translations: Required["_Schema51"]
    """ Required property """


_Schema10 = str
"""
When this word was coined, to precision known.

pattern: ^(?:|(?<year>20\d{2})(?:-(?<month>0[1-9]|1[0-2])(?:-(?<day>0[1-9]|[12]\d|3[01]))?)?|(?<startYear>20\d{2})-(?<endYear>20\d{2}))$
"""


_Schema11 = list["_Schema12"]
""" The name or names of those involved in creating this word. """


_Schema12 = str
""" minLength: 1 """


_Schema14 = dict[str, "_Schema15"]
"""
propertyNames:
  __type__: string
  description: A possible translation of the word into English, as listed in the Toki
    Pona dictionary.
  minLength: 1
"""


_Schema15 = int | float
"""
minimum: 0
maximum: 100
"""


_Schema19 = list["_Schema0"]
""" The IDs of one or more objects related to this one. """


class _Schema20(TypedDict, total=False):
    """Non-Linku resources related to the specific word, such as wiki links."""

    sona_pona: "_Schema22"
    """
    A URL pointing to some external resource.

    format: uri
    """

    lipamanka_semantic: "_Schema22"
    """
    A URL pointing to some external resource.

    format: uri
    """


_Schema22 = str
"""
A URL pointing to some external resource.

format: uri
"""


class _Schema24(TypedDict, total=False):
    """Ways of representing this word via text/computers"""

    sitelen_emosi: "_Schema26"
    """
    minLength: 1
    format: emoji
    pattern: ^(\p{Extended_Pictographic}|\p{Emoji_Component})+$
    """

    sitelen_jelo: "_Schema28"
    """ minItems: 1 """

    ligatures: list["_Schema31Item"]
    sitelen_sitelen: "_Schema22"
    """
    A URL pointing to some external resource.

    format: uri
    """

    ucsur: "_Schema34"
    """ pattern: ^U\+[\da-fA-F]{4,6}$ """


_Schema26 = str
"""
minLength: 1
format: emoji
pattern: ^(\p{Extended_Pictographic}|\p{Emoji_Component})+$
"""


_Schema28 = list["_Schema29"]
""" minItems: 1 """


_Schema29 = str
"""
minLength: 1
format: emoji
pattern: ^(\p{Extended_Pictographic}|\p{Emoji_Component})+$
"""


_Schema3 = str
"""
The latin alphabet representation of the word.

minLength: 1
"""


_Schema31Item = str
""" minLength: 1 """


_Schema34 = str
""" pattern: ^U\+[\da-fA-F]{4,6}$ """


_Schema35 = str
"""
The language this word originated from

minLength: 1
"""


_Schema36 = (
    Literal["core"]
    | Literal["common"]
    | Literal["uncommon"]
    | Literal["obscure"]
    | Literal["sandbox"]
)
""" The word's usage category, derived from the data of the annual Linku word survey. """
_SCHEMA36_CORE: Literal["core"] = "core"
"""The values for the 'The word's usage category, derived from the data of the annual Linku word survey' enum"""
_SCHEMA36_COMMON: Literal["common"] = "common"
"""The values for the 'The word's usage category, derived from the data of the annual Linku word survey' enum"""
_SCHEMA36_UNCOMMON: Literal["uncommon"] = "uncommon"
"""The values for the 'The word's usage category, derived from the data of the annual Linku word survey' enum"""
_SCHEMA36_OBSCURE: Literal["obscure"] = "obscure"
"""The values for the 'The word's usage category, derived from the data of the annual Linku word survey' enum"""
_SCHEMA36_SANDBOX: Literal["sandbox"] = "sandbox"
"""The values for the 'The word's usage category, derived from the data of the annual Linku word survey' enum"""


_Schema37 = bool
""" Whether this word is considered deprecated by its author(s). """


class _Schema38Item(TypedDict, total=False):
    """Audio files of the words pronounced out loud"""

    author: Required["_Schema12"]
    """
    minLength: 1

    Required property
    """

    link: Required["_Schema22"]
    """
    A URL pointing to some external resource.

    format: uri

    Required property
    """


class _Schema42(TypedDict, total=False):
    en: Required["_Schema43"]
    """
    Localized definition on the parent, such as a word or luka pona sign

    minLength: 1

    Required property
    """

    fr: Required["_Schema43"]
    """
    Localized definition on the parent, such as a word or luka pona sign

    minLength: 1

    Required property
    """

    de: Required["_Schema43"]
    """
    Localized definition on the parent, such as a word or luka pona sign

    minLength: 1

    Required property
    """

    eo: Required["_Schema43"]
    """
    Localized definition on the parent, such as a word or luka pona sign

    minLength: 1

    Required property
    """


_Schema43 = str
"""
Localized definition on the parent, such as a word or luka pona sign

minLength: 1
"""


_Schema44 = dict[str, "_Schema15"]
"""
The percentage of respondents to the annual Linku word survey who report to use this word, by the date of the survey.

propertyNames:
  $ref: '#/$defs/__schema45'
"""


class _Schema51(TypedDict, total=False):
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

    definition: Required["_Schema43"]
    """
    Localized definition on the parent, such as a word or luka pona sign

    minLength: 1

    Required property
    """


_Schema7 = str
""" The source or origin of this object, often a URL. """


_Schema8 = Literal["pu"] | Literal["ku suli"] | Literal["ku lili"] | Literal["none"]
""" Which official Toki Pona book was this word featured in, if any. """
_SCHEMA8_PU: Literal["pu"] = "pu"
"""The values for the 'Which official Toki Pona book was this word featured in, if any' enum"""
_SCHEMA8_KU_SULI: Literal["ku suli"] = "ku suli"
"""The values for the 'Which official Toki Pona book was this word featured in, if any' enum"""
_SCHEMA8_KU_LILI: Literal["ku lili"] = "ku lili"
"""The values for the 'Which official Toki Pona book was this word featured in, if any' enum"""
_SCHEMA8_NONE: Literal["none"] = "none"
"""The values for the 'Which official Toki Pona book was this word featured in, if any' enum"""


_Schema9 = Literal["pre-pu"] | Literal["post-pu"] | Literal["post-ku"]
""" The period of time in which this word was coined, relative to the publication of the first two official Toki Pona books """
_SCHEMA9_PRE_PU: Literal["pre-pu"] = "pre-pu"
"""The values for the 'The period of time in which this word was coined, relative to the publication of the first two official Toki Pona books' enum"""
_SCHEMA9_POST_PU: Literal["post-pu"] = "post-pu"
"""The values for the 'The period of time in which this word was coined, relative to the publication of the first two official Toki Pona books' enum"""
_SCHEMA9_POST_KU: Literal["post-ku"] = "post-ku"
"""The values for the 'The period of time in which this word was coined, relative to the publication of the first two official Toki Pona books' enum"""
