import re
from collections.abc import Callable

from ilo.jasima import bundle, get_word_entry
from ilo.tokenizer import SENT_DELIMITERS, tokenize

bundle = bundle["data"]

SYMBOL_RE = r"[^a-zA-Z]*"
SYMBOL_RE = re.compile(SYMBOL_RE)

ETYM_RE = r"^(?P<word>.+) (?:‘(?P<definition>.*)’)?(?:\((?P<alttext>.*)\))?"
# TODO: incomplete, waiting on consistent format in jasima
MULTI_ETYM_RE = rf""

EN_SPECIAL_CASES = {
    "li": "is",
    "e": "the",
    "ju": "reserved",
    "ku": "interact with Toki Pona Dictionary",
    "lu": "reserved",
    "nu": "reserved",
    "pu": "interact with Toki Pona: The Language of Good",
    "su": "reserved",
    "u": "reserved",
}
ETYM_UNK = {"∅", "?", "unknown"}


def __filter_only_alpha(text: str) -> str:
    return re.sub(SYMBOL_RE, "", text)


def __get_nth_word(defin: str, n: int = 0) -> str:
    return defin.split(" ")[n]


def relex_word_en(word: str) -> str:
    """
    Relex a given word with the following priority order:
    1. special cases
    2. first word of ku data
    3. first word of definition
    4. original input (do nothing)

    This is not reasonable to reverse at present. jasima needs a relex column.
    """
    found = bundle.get(word)
    if not found:
        return word
    if word in EN_SPECIAL_CASES:
        return EN_SPECIAL_CASES[word]
    fetch_from = found.get("ku_data") or found["def"]["en"] if found else word
    word = __filter_only_alpha(__get_nth_word(fetch_from))
    return word


def relex_word_etym(word: str) -> str:
    if not (found := bundle.get(word)):
        return word
    if not (etym_data := found.get("etymology_data")):
        return word
    if not (etym_words := etym_data.get("words")):
        return word

    # remove strip when lipu-linku/jasima/pull/4 is merged
    candidate = etym_words.split(";")[0].strip()
    return candidate


def __sent_relex(input: str, relex_func: Callable) -> str:
    sents_of_words = tokenize(input)
    reconstructed = ""
    for sent in sents_of_words:
        to_reconstruct = [relex_func(word) or word for word in sent[:-1]]
        reconstructed += " ".join(to_reconstruct)

        # the last is punct if punct is present
        # else it's a word to relex
        final = sent[-1]
        if final in SENT_DELIMITERS:
            reconstructed += final + " "
        else:
            reconstructed += " " + relex_func(final)
            # last item whatsoever
    return reconstructed


def relex_sent_etym(input: str):
    return __sent_relex(input, relex_word_etym)


def relex_sent_en(input: str):
    return __sent_relex(input, relex_word_en)


RELEX_FUNC_MAP = {"en": relex_sent_en, "etym": relex_sent_etym}


# mostly for Discord's benefit
def relex(input: str, method: str):
    return RELEX_FUNC_MAP[method](input)
