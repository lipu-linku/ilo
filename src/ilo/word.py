from typing import TYPE_CHECKING, cast

import msgspec

from ilo import data
from sona.word import Word as SonaWord
from sona.word_dataclass import Word as SonaWordDataclass

if TYPE_CHECKING:
    WordBase = SonaWordDataclass
else:
    WordBase = object

class Word(WordBase):
    def __init__(self, json: SonaWord):
        self._data = msgspec.convert(json, SonaWordDataclass)

        self._commentary: dict[str, str] = {}
        self._definition: dict[str, str] = {}
        self._etymology: dict[str, str] = {}

    if not TYPE_CHECKING:
        def __getattr__(self, name: str):
            return getattr(self._data, name)

    @property
    def string(self) -> str:
        return self._data.word

    def add_lang(self, lang: str, json: SonaWord):
        self._commentary[lang] = json["translations"]["commentary"]
        self._definition[lang] = json["translations"]["definition"]
        self._etymology[lang] = json["translations"]["etymology"]

    def get_usage(self) -> float:
        return next(reversed(self.usage.values())) if self.usage else 0

    def get_commentary(self, lang: str = "en") -> str:
        data.fetch_lang(lang)
        return self._commentary[lang]

    def get_definition(self, lang: str = "en") -> str:
        data.fetch_lang(lang)
        return self._definition[lang]

    def get_etymology(self, lang: str = "en") -> str:
        data.fetch_lang(lang)
        return self._etymology[lang]
