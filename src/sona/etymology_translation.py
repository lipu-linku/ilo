# Generated from the JSON schema of sona Linku


from typing import Dict, List, Required, TypedDict

EtymologyTranslation = Dict[str, List["_EtymologytranslationAdditionalpropertiesItem"]]
""" Localized etymological values for Toki Pona words """


class _EtymologytranslationAdditionalpropertiesItem(TypedDict, total=False):
    definition: str
    """ The localized definition of the root word in its origin language """

    language: Required[str]
    """
    The localized name of the language this word originated from

    Required property
    """
