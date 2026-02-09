import csv
from typing import TypeVar, Optional
from dataclasses import dataclass, field


@dataclass
class CsvDefs:
    times_asked: str
    submitted: str
    keyword: str
    pos: str
    enumeration: str
    tok: str
    eng: str
    examples: str


@dataclass
class CsvNotes:
    submitted: str
    keyword: str
    notes: str


@dataclass
class Example:
    tok: str
    eng: str


@dataclass
class Definition:
    tok: str
    eng: str
    pos: str
    enumeration: str
    examples: Optional[list[Example]] = None


@dataclass
class KemekaEntry:
    keyword: str
    definitions: list[Definition] = field(default_factory=list)
    notes: Optional[str] = None


T = TypeVar("T")


def from_csv(Type: type[T], path: str) -> list[T]:
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        reader.fieldnames = [
            name.replace(" ", "_") if name else name
            for name in reader.fieldnames  # pyright: ignore[reportOptionalIterable]
        ]
        return [Type(**row) for row in reader]


def load_kemeka_data() -> list[KemekaEntry]:
    notes = from_csv(CsvNotes, "kemeka/data/notes.csv")
    defs = from_csv(CsvDefs, "kemeka/data/definitions.csv")

    defs = [
        row for row in defs if row.tok != "" and row.eng != "" and row.examples != ""
    ]

    entries: dict[str, KemekaEntry] = {}

    for row in defs:
        keyword = row.keyword

        if keyword not in entries:
            note = next((note.notes for note in notes if note.keyword == keyword), None)
            entries[keyword] = KemekaEntry(keyword=keyword, definitions=[], notes=note)

        examples = None
        if row.examples:
            if row.examples.strip():
                examples = []
                for example in row.examples.strip().split("\n"):
                    parts = example.split(" | ")
                    if len(parts) == 2:
                        examples.append(Example(tok=parts[0], eng=parts[1]))

        entries[keyword].definitions.append(
            Definition(
                tok=row.tok,
                eng=row.eng,
                pos=row.pos,
                enumeration=row.enumeration,
                examples=examples,
            )
        )

    return list(entries.values())
