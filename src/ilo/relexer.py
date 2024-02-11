from collections.abc import Callable

from ilo.data import Dict, deep_get_word_data, get_word_data
from ilo.tokenizer import SENT_DELIMITERS, tokenize

EN_SPECIAL_CASES = {
    "li": "is",
    "e": "the",
    "ju": "reserved",
    "ku": "interact with Toki Pona Dictionary",
    "lu": "reserved",
    "nu": "reserved",
    "pu": "interact with Toki Pona: The Language of Good",
    "su": "interact with a book from the illustrated story book series that began with The Wonderful Wizard of Oz, produced by Sonja Lang",
    "u": "reserved",
}


def __get_highest_scoring(word: str, ku_data: Dict[str, int]):
    score = 0
    for k, v in ku_data.items():
        if v > score:
            word, score = k, v
    return word


def relex_word_en(word: str) -> str:
    """
    Relex a given word with the following priority order:
    1. special cases
    2. highest scoring word of ku data
    3. original input (do nothing)

    This is not reasonable to reverse at present. sona would need a relex column.
    """
    found = get_word_data(word)
    if not found:
        return word
    if word in EN_SPECIAL_CASES:
        return EN_SPECIAL_CASES[word]
    if "ku_data" in found:  # TODO: typing garbagefire
        return __get_highest_scoring(word, found["ku_data"])
    return word


def relex_word_etym(word: str) -> str:
    return deep_get_word_data(word, "etymology", 0, "word") or word


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
