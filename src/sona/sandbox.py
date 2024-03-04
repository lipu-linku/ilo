# Generated from the JSON schema of sona Linku


from typing import Dict, List, Literal, Required, TypedDict, Union

Sandbox = Dict[str, "_SandboxAdditionalproperties"]
"""
A raw data object containing dictionary info about Toki Pona sandbox

propertyNames:
  minLength: 1
"""


class _SandboxAdditionalproperties(TypedDict, total=False):
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

    book: Required["_SandboxAdditionalpropertiesBook"]
    """
    Which official Toki Pona book was this word featured in, if any.

    Required property
    """

    coined_era: Required["_SandboxAdditionalpropertiesCoinedEra"]
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

    ku_data: Dict[str, "_SandboxAdditionalpropertiesKuDataAdditionalproperties"]
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

    resources: "_SandboxAdditionalpropertiesResources"
    """ Non-Linku resources related to the specific word, such as wiki links. """

    representations: "_SandboxAdditionalpropertiesRepresentations"
    """ Ways of representing this word in the real world, via text/computers """

    source_language: Required[str]
    """
    The language this word originated from

    Required property
    """

    usage_category: Required["_SandboxAdditionalpropertiesUsageCategory"]
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

    etymology: Required[List["_SandboxAdditionalpropertiesEtymologyItem"]]
    """
    Unlocalized etymological values regarding this word's origin

    Required property
    """

    audio: Required[List["_SandboxAdditionalpropertiesAudioItem"]]
    """ Required property """

    pu_verbatim: "_SandboxAdditionalpropertiesPuVerbatim"
    """ The original definition of the word in pu, the first official Toki Pona book """

    usage: Required[Dict[str, "_SandboxAdditionalpropertiesUsageAdditionalproperties"]]
    """
    The percentage of people in the Toki Pona community who use this word, according to surveys performed by the Linku Project

    propertyNames:
      pattern: ^20\d{2}-(0[1-9]|1[0-2])$

    Required property
    """

    translations: Required[
        Dict[str, "_SandboxAdditionalpropertiesTranslationsAdditionalproperties"]
    ]
    """ Required property """


class _SandboxAdditionalpropertiesAudioItem(TypedDict, total=False):
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


_SandboxAdditionalpropertiesBook = Union[
    Literal["pu"], Literal["ku suli"], Literal["ku lili"], Literal["none"]
]
""" Which official Toki Pona book was this word featured in, if any. """
_SANDBOXADDITIONALPROPERTIESBOOK_PU: Literal["pu"] = "pu"
"""The values for the 'Which official Toki Pona book was this word featured in, if any' enum"""
_SANDBOXADDITIONALPROPERTIESBOOK_KU_SULI: Literal["ku suli"] = "ku suli"
"""The values for the 'Which official Toki Pona book was this word featured in, if any' enum"""
_SANDBOXADDITIONALPROPERTIESBOOK_KU_LILI: Literal["ku lili"] = "ku lili"
"""The values for the 'Which official Toki Pona book was this word featured in, if any' enum"""
_SANDBOXADDITIONALPROPERTIESBOOK_NONE: Literal["none"] = "none"
"""The values for the 'Which official Toki Pona book was this word featured in, if any' enum"""


_SandboxAdditionalpropertiesCoinedEra = Union[
    "_SandboxAdditionalpropertiesCoinedEraAnyof0", Literal[""]
]
"""
When this word was coined (relative to the publication dates of the official Toki Pona books, if known)

Aggregation type: anyOf
"""


_SandboxAdditionalpropertiesCoinedEraAnyof0 = Union[
    Literal["pre-pu"], Literal["post-pu"], Literal["post-ku"]
]
_SANDBOXADDITIONALPROPERTIESCOINEDERAANYOF0_PRE_PU: Literal["pre-pu"] = "pre-pu"
"""The values for the '_SandboxAdditionalpropertiesCoinedEraAnyof0' enum"""
_SANDBOXADDITIONALPROPERTIESCOINEDERAANYOF0_POST_PU: Literal["post-pu"] = "post-pu"
"""The values for the '_SandboxAdditionalpropertiesCoinedEraAnyof0' enum"""
_SANDBOXADDITIONALPROPERTIESCOINEDERAANYOF0_POST_KU: Literal["post-ku"] = "post-ku"
"""The values for the '_SandboxAdditionalpropertiesCoinedEraAnyof0' enum"""


class _SandboxAdditionalpropertiesEtymologyItem(TypedDict, total=False):
    word: str
    """ One of the root words of this word, as written out in its language of origin """

    alt: str
    """ A latinized representation of the "word" field """


_SandboxAdditionalpropertiesKuDataAdditionalproperties = Union[int, float]
"""
The percentage of ku survey respondents who report this translation as accurate to their usage.

minimum: 0
maximum: 100
"""


class _SandboxAdditionalpropertiesPuVerbatim(TypedDict, total=False):
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


class _SandboxAdditionalpropertiesRepresentations(TypedDict, total=False):
    """Ways of representing this word in the real world, via text/computers"""

    sitelen_emosi: str
    """
    The sitelen emosi representation of this word, a script for writing Toki Pona using emoji

    pattern: ^(\p{Extended_Pictographic}|\p{Emoji_Component})+$
    """

    sitelen_jelo: List["_SandboxAdditionalpropertiesRepresentationsSitelenJeloItem"]
    """
    One or more example emojis for how the word can be written in sitelen jelo

    minItems: 1
    """

    ligatures: List["_SandboxAdditionalpropertiesRepresentationsLigaturesItem"]
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


_SandboxAdditionalpropertiesRepresentationsLigaturesItem = str
""" minLength: 1 """


_SandboxAdditionalpropertiesRepresentationsSitelenJeloItem = str
""" pattern: ^(\p{Extended_Pictographic}|\p{Emoji_Component})+$ """


class _SandboxAdditionalpropertiesResources(TypedDict, total=False):
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


class _SandboxAdditionalpropertiesTranslationsAdditionalproperties(
    TypedDict, total=False
):
    commentary: Required[str]
    """ Required property """

    definition: Required[str]
    """
    minLength: 1

    Required property
    """

    etymology: Required[
        List[
            "_SandboxAdditionalpropertiesTranslationsAdditionalpropertiesEtymologyItem"
        ]
    ]
    """ Required property """

    sp_etymology: Required[str]
    """ Required property """


class _SandboxAdditionalpropertiesTranslationsAdditionalpropertiesEtymologyItem(
    TypedDict, total=False
):
    definition: str
    """ The localized definition of the root word in its origin language """

    language: Required[str]
    """
    The localized name of the language this word originated from

    Required property
    """


_SandboxAdditionalpropertiesUsageAdditionalproperties = Union[int, float]
"""
minimum: 0
maximum: 100
"""


_SandboxAdditionalpropertiesUsageCategory = Union[
    Literal["core"],
    Literal["common"],
    Literal["uncommon"],
    Literal["obscure"],
    Literal["sandbox"],
]
""" The word's usage category, according to a survey performed by the Linku Project """
_SANDBOXADDITIONALPROPERTIESUSAGECATEGORY_CORE: Literal["core"] = "core"
"""The values for the 'The word's usage category, according to a survey performed by the Linku Project' enum"""
_SANDBOXADDITIONALPROPERTIESUSAGECATEGORY_COMMON: Literal["common"] = "common"
"""The values for the 'The word's usage category, according to a survey performed by the Linku Project' enum"""
_SANDBOXADDITIONALPROPERTIESUSAGECATEGORY_UNCOMMON: Literal["uncommon"] = "uncommon"
"""The values for the 'The word's usage category, according to a survey performed by the Linku Project' enum"""
_SANDBOXADDITIONALPROPERTIESUSAGECATEGORY_OBSCURE: Literal["obscure"] = "obscure"
"""The values for the 'The word's usage category, according to a survey performed by the Linku Project' enum"""
_SANDBOXADDITIONALPROPERTIESUSAGECATEGORY_SANDBOX: Literal["sandbox"] = "sandbox"
"""The values for the 'The word's usage category, according to a survey performed by the Linku Project' enum"""
