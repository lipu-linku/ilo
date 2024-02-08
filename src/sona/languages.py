# Generated from the JSON schema of sona Linku


from typing import Dict, Required, TypedDict

Languages = Dict[str, "_LanguagesAdditionalproperties"]
"""
propertyNames:
  minLength: 2
"""


class _LanguagesAdditionalproperties(TypedDict, total=False):
    """The languages offered by sona Linku."""

    locale: Required[str]
    """
    The locale code corresponding to the language.

    Required property
    """

    name: Required["_LanguagesAdditionalpropertiesName"]
    """ Required property """


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
