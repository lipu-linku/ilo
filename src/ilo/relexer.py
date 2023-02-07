from ilo.defines import relex_map
from ilo.tokenizer import SENT_DELIMITERS, tokenize


def get_relex(word: str, lang: str) -> str:
    found = relex_map.get(word)
    word = found[lang] if found else word
    return word


def relex(input: str, lang: str):
    # TODO: derive relex from jasima defs somehow?

    lang = "en"

    sents_of_words = tokenize(input)
    reconstructed = ""
    for sent in sents_of_words:
        to_reconstruct = [get_relex(word, lang) for word in sent[:-1]]
        reconstructed += " ".join(to_reconstruct)

        # the last is punct if punct is present
        # else it's a word to relex
        final = sent[-1]
        if final in SENT_DELIMITERS:
            reconstructed += final + " "
        else:
            reconstructed += " " + get_relex(final, lang)
            # last item whatsoever
    return reconstructed
