import pytest

from ilo.relexer import relex_word_en, relex_word_etym

all_words = [
    "a",
    "aka",
    "akesi",
    "ako",
    "ala",
    "alasa",
    "ale",
    "alente",
    "ali",
    "alu",
    "anpa",
    "ante",
    "anu",
    "apeja",
    "awase",
    "awen",
    "e",
    "eki",
    "en",
    "enko",
    "epiku",
    "esun",
    "ete",
    "ewe",
    "i",
    "ijo",
    "ike",
    "iki",
    "ilo",
    "insa",
    "ipi",
    "isipin",
    "itomi",
    "jaki",
    "jaku",
    "jalan",
    "jami",
    "jan",
    "jans",
    "jasima",
    "je",
    "jelo",
    "jo",
    "jonke",
    "ju",
    "jule",
    "jume",
    "kala",
    "kalama",
    "kalamARR",
    "kalijopilale",
    "kama",
    "kamalawala",
    "kan",
    "kapa",
    "kapesi",
    "kasi",
    "ke",
    "ken",
    "kepeken",
    "kepen",
    "kese",
    "ki",
    "kijetesantakalu",
    "kiki",
    "kili",
    "kin",
    "kipisi",
    "kisa",
    "kiwen",
    "ko",
    "kokosila",
    "kon",
    "konsi",
    "konwe",
    "kosan",
    "ku",
    "kule",
    "kulijo",
    "kulu",
    "kulupu",
    "kuntu",
    "kute",
    "kutopoma",
    "la",
    "lanpan",
    "lape",
    "laso",
    "lawa",
    "leko",
    "len",
    "lete",
    "li",
    "lijokuku",
    "likujo",
    "lili",
    "linja",
    "linluwi",
    "lipu",
    "lo",
    "loje",
    "loka",
    "lokon",
    "lon",
    "lu",
    "luka",
    "lukin",
    "lupa",
    "ma",
    "majuna",
    "mama",
    "mani",
    "meli",
    "melome",
    "meso",
    "mi",
    "mije",
    "mijomi",
    "misa",
    "misikeke",
    "moku",
    "moli",
    "molusa",
    "monsi",
    "monsuta",
    "mu",
    "mulapisu",
    "mun",
    "musi",
    "mute",
    "n",
    "nalanja",
    "namako",
    "nanpa",
    "nasa",
    "nasin",
    "natu",
    "neja",
    "nele",
    "nena",
    "ni",
    "nimi",
    "nimisin",
    "nja",
    "noka",
    "nu",
    "o",
    "ojuta",
    "oke",
    "okepuma",
    "oki",
    "oko",
    "olin",
    "omekalike",
    "omekapo",
    "omen",
    "ona",
    "oni",
    "open",
    "owe",
    "pa",
    "pakala",
    "pake",
    "pali",
    "palisa",
    "pan",
    "pana",
    "pasila",
    "pata",
    "peta",
    "peto",
    "pi",
    "pika",
    "pilin",
    "pimeja",
    "Pingo",
    "pini",
    "pipi",
    "pipo",
    "po",
    "poka",
    "poki",
    "polinpin",
    "pomotolo",
    "pona",
    "poni",
    "powe",
    "pu",
    "puwa",
    "sama",
    "samu",
    "san",
    "seli",
    "selo",
    "seme",
    "sewi",
    "sijelo",
    "sike",
    "sikomo",
    "sin",
    "sina",
    "sinpin",
    "sipi",
    "sitelen",
    "slape",
    "soko",
    "sona",
    "soto",
    "soweli",
    "su",
    "suke",
    "suli",
    "suno",
    "supa",
    "sutopatikuna",
    "suwi",
    "taki",
    "tan",
    "taso",
    "tawa",
    "te",
    "teje",
    "telo",
    "ten",
    "tenpo",
    "to",
    "tokana",
    "toki",
    "toma",
    "tomo",
    "tonsi",
    "tu",
    "tuli",
    "u",
    "umesu",
    "unpa",
    "unu",
    "usawi",
    "uta",
    "utala",
    "wa",
    "waleja",
    "walo",
    "wan",
    "waso",
    "wasoweli",
    "wawa",
    "wawajete",
    "we",
    "weka",
    "wekama",
    "wi",
    "wile",
    "wuwojiti",
    "yupekosi",
    "yutu",
]


@pytest.mark.parametrize("relexer", [relex_word_etym, relex_word_en])
def test_english(relexer):
    for word in all_words:
        relexed = relexer(word)
        # print(f"{word:<15} {relexed:<15}")
        assert relexed