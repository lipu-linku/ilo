# Generated from the JSON schema of sona Linku


from typing import Literal, Required, TypedDict


class Language(TypedDict, total=False):
    id: Required["_Schema0"]
    """
    A unique identifier for an object in Linku. Generally named after the object.

    minLength: 1

    Required property
    """

    locale: Required["_Schema0"]
    """
    A unique identifier for an object in Linku. Generally named after the object.

    minLength: 1

    Required property
    """

    direction: Required["_LanguageDirection"]
    """
    The direction of the language's script.

    Aggregation type: anyOf

    Required property
    """

    name: Required["_LanguageName"]
    """ Required property """


_LanguageDirection = Literal["ltr"] | Literal["rtl"]
"""
The direction of the language's script.

Aggregation type: anyOf
"""


class _LanguageName(TypedDict, total=False):
    en: Required[str]
    """
    The name of the language in English.

    Required property
    """

    endonym: Required[str]
    """
    The name of the language in that language. Prefer if available.

    Required property
    """

    tok: str


_Schema0 = str
"""
A unique identifier for an object in Linku. Generally named after the object.

minLength: 1
"""
