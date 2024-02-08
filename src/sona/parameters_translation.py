# Generated from the JSON schema of sona Linku


from typing import Dict, TypedDict

ParametersTranslation = Dict[str, "_ParameterstranslationAdditionalproperties"]
"""
Partly localized descriptions of how a sign is signed.

propertyNames:
  minLength: 1
"""


class _ParameterstranslationAdditionalproperties(TypedDict, total=False):
    handshape: str
    """ The shape of the hand when signing, identified by its name in ASL. Should not be translated in any language other than Toki Pona """

    movement: str
    """ The motion of the hand when signing. """

    placement: str
    """ The placement of the hand when signing. """

    orientation: str
    """ The orientation of the hand when signing. """
