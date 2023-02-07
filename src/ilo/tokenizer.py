import re

SENT_DELIMITERS = r".?!;:"
SENT_DELIMITERS_RE = rf".*?[{SENT_DELIMITERS}]"
SENT_DELIMITERS_RE = re.compile(SENT_DELIMITERS_RE)
WORD_DELIMITERS = r".?!;:,-"
WORD_DELIMITERS_RE = rf"\s+|(?=[{WORD_DELIMITERS}])"
WORD_DELIMITERS_RE = re.compile(WORD_DELIMITERS_RE)


def _sent_tokenize(text: str) -> list[str]:
    sents = [sent.strip() for sent in re.findall(SENT_DELIMITERS_RE, text)]

    # TODO: we can do better than this lmao
    final = re.split(SENT_DELIMITERS_RE, text)[-1].strip()
    if final:  # catch non-punct final sentence
        sents += [final]
    return sents


def _word_tokenize(text: str) -> list[str]:
    words = [word.strip() for word in re.split(WORD_DELIMITERS_RE, text)]
    if not words:
        words = [text]  # ditto
    return words


def tokenize(text: str) -> list[list[str]]:
    sentences = _sent_tokenize(text)
    words = [_word_tokenize(sentence) for sentence in sentences]
    return words
