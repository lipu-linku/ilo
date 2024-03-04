# Generated from the JSON schema of sona Linku


from typing import Dict, List, Literal, Required, TypedDict, Union


class Word(TypedDict, total=False):
    """General info on a Toki Pona word"""

    id: Required[str]
    """
    A unique identifier for the word. Usually the word but may have an integer added in case of a word with multiple definitions (like "we")

    minLength: 1

    Required property
    """

    author_verbatim: Required[str]
    """
    The author's original definition, taken verbatim in their words

    Required property
    """

    author_verbatim_source: Required[str]
    """
    Where the author's original definition is located (usually Discord)

    Required property
    """

    book: Required["_WordBook"]
    """
    Which official Toki Pona book was this word featured in, if any.

    Required property
    """

    coined_era: Required["_WordCoinedEra"]
    """
    When this word was coined (relative to the publication dates of the official Toki Pona books, if known)

    Aggregation type: anyOf

    Required property
    """

    coined_year: Required[str]
    """
    The year when this word was coined (if known)

    Required property
    """

    creator: Required[List[str]]
    """
    The person who created this word (if known)

    Required property
    """

    ku_data: Dict[str, "_WordKuDataAdditionalproperties"]
    """
    The usage data of the word as described in ku (the official Toki Pona dictionary)

    propertyNames:
      minLength: 1
    """

    see_also: Required[List[str]]
    """
    A list of related words

    Required property
    """

    resources: "_WordResources"
    """ Non-Linku resources related to the specific word, such as wiki links. """

    representations: "_WordRepresentations"
    """ Ways of representing this word in the real world, via text/computers """

    source_language: Required[str]
    """
    The language this word originated from

    Required property
    """

    usage_category: Required["_WordUsageCategory"]
    """
    The word's usage category, according to a survey performed by the Linku Project

    Required property
    """

    word: Required[str]
    """
    The word's actual text, in case of a word with multiple definitions (like "we")

    Required property
    """

    deprecated: Required[bool]
    """
    Whether or not the word is considered deprecated by its author.

    Required property
    """

    etymology: Required[List["_WordEtymologyItem"]]
    """
    Unlocalized etymological values regarding this word's origin

    Required property
    """

    audio: Required[List["_WordAudioItem"]]
    """ Required property """

    pu_verbatim: "_WordPuVerbatim"
    """ The original definition of the word in pu, the first official Toki Pona book """

    usage: Required[Dict[str, "_WordUsageAdditionalproperties"]]
    """
    The percentage of people in the Toki Pona community who use this word, according to surveys performed by the Linku Project

    propertyNames:
      pattern: ^20\d{2}-(0[1-9]|1[0-2])$

    Required property
    """


class _WordAudioItem(TypedDict, total=False):
    """Audio files of the words pronounced out loud"""

    author: Required[str]
    """
    The author of the audio file in `link`.

    Required property
    """

    link: Required[str]
    """
    A link to the audio file for the word, pronounced by `author`.

    format: uri

    Required property
    """


_WordBook = Union[
    Literal["pu"], Literal["ku suli"], Literal["ku lili"], Literal["none"]
]
""" Which official Toki Pona book was this word featured in, if any. """
_WORDBOOK_PU: Literal["pu"] = "pu"
"""The values for the 'Which official Toki Pona book was this word featured in, if any' enum"""
_WORDBOOK_KU_SULI: Literal["ku suli"] = "ku suli"
"""The values for the 'Which official Toki Pona book was this word featured in, if any' enum"""
_WORDBOOK_KU_LILI: Literal["ku lili"] = "ku lili"
"""The values for the 'Which official Toki Pona book was this word featured in, if any' enum"""
_WORDBOOK_NONE: Literal["none"] = "none"
"""The values for the 'Which official Toki Pona book was this word featured in, if any' enum"""


_WordCoinedEra = Union["_WordCoinedEraAnyof0", Literal[""]]
"""
When this word was coined (relative to the publication dates of the official Toki Pona books, if known)

Aggregation type: anyOf
"""


_WordCoinedEraAnyof0 = Union[Literal["pre-pu"], Literal["post-pu"], Literal["post-ku"]]
_WORDCOINEDERAANYOF0_PRE_PU: Literal["pre-pu"] = "pre-pu"
"""The values for the '_WordCoinedEraAnyof0' enum"""
_WORDCOINEDERAANYOF0_POST_PU: Literal["post-pu"] = "post-pu"
"""The values for the '_WordCoinedEraAnyof0' enum"""
_WORDCOINEDERAANYOF0_POST_KU: Literal["post-ku"] = "post-ku"
"""The values for the '_WordCoinedEraAnyof0' enum"""


class _WordEtymologyItem(TypedDict, total=False):
    word: str
    """ One of the root words of this word, as written out in its language of origin """

    alt: str
    """ A latinized representation of the "word" field """


_WordKuDataAdditionalproperties = Union[int, float]
"""
The percentage of ku survey respondents who report this translation as accurate to their usage.

minimum: 0
maximum: 100
"""


class _WordPuVerbatim(TypedDict, total=False):
    """The original definition of the word in pu, the first official Toki Pona book"""

    en: Required[str]
    """
    The original definition in the English version of pu

    Required property
    """

    fr: Required[str]
    """
    The original definition in the French version of pu

    Required property
    """

    de: Required[str]
    """
    The original definition in the German version of pu

    Required property
    """

    eo: Required[str]
    """
    The original definition in the Esperanto version of pu

    Required property
    """


class _WordRepresentations(TypedDict, total=False):
    """Ways of representing this word in the real world, via text/computers"""

    sitelen_emosi: str
    """
    The sitelen emosi representation of this word, a script for writing Toki Pona using emoji

    pattern: ^(\p{Extended_Pictographic}|\p{Emoji_Component})+$
    """

    sitelen_jelo: List["_WordRepresentationsSitelenJeloItem"]
    """
    One or more example emojis for how the word can be written in sitelen jelo

    minItems: 1
    """

    ligatures: List["_WordRepresentationsLigaturesItem"]
    """ A list of sitelen Lasina representations of the word, used by ligature fonts to visually convert latin characters into sitelen pona """

    sitelen_sitelen: str
    """
    A URL pointing to an image of this word's sitelen sitelen hieroglyphic block

    format: uri
    """

    ucsur: str
    """
    The word's UCSUR codepoint, as defined in https://www.kreativekorp.com/ucsur/charts/sitelen.html

    pattern: ^U\+[\da-fA-F]{4,6}$
    """


_WordRepresentationsLigaturesItem = str
""" minLength: 1 """


_WordRepresentationsSitelenJeloItem = str
""" pattern: ^(\p{Extended_Pictographic}|\p{Emoji_Component})+$ """


class _WordResources(TypedDict, total=False):
    """Non-Linku resources related to the specific word, such as wiki links."""

    sona_pona: str
    """
    A link to the word's page on sona.pona.la, a Toki Pona wiki. May redirect for words with references but no dedicated page.

    format: uri
    """

    lipamanka_semantic: str
    """
    A link to lipamanka's description of the word's semantic space.

    format: uri
    """


_WordUsageAdditionalproperties = Union[int, float]
"""
minimum: 0
maximum: 100
"""


_WordUsageCategory = Union[
    Literal["core"],
    Literal["common"],
    Literal["uncommon"],
    Literal["obscure"],
    Literal["sandbox"],
]
""" The word's usage category, according to a survey performed by the Linku Project """
_WORDUSAGECATEGORY_CORE: Literal["core"] = "core"
"""The values for the 'The word's usage category, according to a survey performed by the Linku Project' enum"""
_WORDUSAGECATEGORY_COMMON: Literal["common"] = "common"
"""The values for the 'The word's usage category, according to a survey performed by the Linku Project' enum"""
_WORDUSAGECATEGORY_UNCOMMON: Literal["uncommon"] = "uncommon"
"""The values for the 'The word's usage category, according to a survey performed by the Linku Project' enum"""
_WORDUSAGECATEGORY_OBSCURE: Literal["obscure"] = "obscure"
"""The values for the 'The word's usage category, according to a survey performed by the Linku Project' enum"""
_WORDUSAGECATEGORY_SANDBOX: Literal["sandbox"] = "sandbox"
"""The values for the 'The word's usage category, according to a survey performed by the Linku Project' enum"""
