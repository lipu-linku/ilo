# Generated from the JSON schema of sona Linku


from typing import Dict, Literal, Required, TypedDict, Union

Languages = Dict[str, "_LanguagesAdditionalproperties"]
"""
propertyNames:
  minLength: 2
"""


class _LanguagesAdditionalproperties(TypedDict, total=False):
    """The languages offered by sona Linku."""

    id: Required[str]
    """
    The language code used by Crowdin. Approximates 2 letter code -> 3 letter code.

    minLength: 2

    Required property
    """

    locale: Required[str]
    """
    The locale code corresponding to the language.

    Required property
    """

    direction: Required["_LanguagesAdditionalpropertiesDirection"]
    """
    The direction of the language's script.

    Required property
    """

    name: Required["_LanguagesAdditionalpropertiesName"]
    """ Required property """


_LanguagesAdditionalpropertiesDirection = Union[Literal["ltr"], Literal["rtl"]]
""" The direction of the language's script. """
_LANGUAGESADDITIONALPROPERTIESDIRECTION_LTR: Literal["ltr"] = "ltr"
"""The values for the 'The direction of the language's script' enum"""
_LANGUAGESADDITIONALPROPERTIESDIRECTION_RTL: Literal["rtl"] = "rtl"
"""The values for the 'The direction of the language's script' enum"""


class _LanguagesAdditionalpropertiesName(TypedDict, total=False):
    en: Required[str]
    """
    The name of the language in English.

    Required property
    """

    tok: str
    """ The name of the language in Toki Pona. """

    endonym: str
    """ The name of the language in that language. """
