from typing import cast

from ilo import data
from sona.word import Word as SonaWord


class Word:
    def __init__(self, json: SonaWord):
        self._data: SonaWord = json

        self._commentary: dict[str, str] = {}
        self._definition: dict[str, str] = {}
        self._etymology: dict[str, str] = {}

    def __getattr__(self, name: str):
        try:
            return self._data[name]
        except KeyError:
            raise AttributeError(name) from None

    @property
    def string(self) -> str:
        return cast(str, self._data["word"])

    def add_lang(self, lang: str, json: SonaWord):
        self._commentary[lang] = json["translations"]["commentary"]
        self._definition[lang] = json["translations"]["definition"]
        self._etymology[lang] = json["translations"]["etymology"]

    def get_usage(self) -> int:
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
