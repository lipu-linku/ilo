import pytest

from ilo.tokenizer import _sent_tokenize, _word_tokenize, tokenize

# parametrize is in case we add alt tokenizers, like nltk, spaCy, gensim


@pytest.mark.parametrize("tokenizer", [_sent_tokenize])
def test_document(tokenizer):
    doc = "mi jan Wiku. sina wile seme? mi wile pona tawa jan mute mute a!"
    compare = [
        "mi jan Wiku.",
        "sina wile seme?",
        "mi wile pona tawa jan mute mute a!",
    ]
    result = tokenizer(doc)
    assert compare == result


@pytest.mark.parametrize("tokenizer", [_sent_tokenize])
def test_single_word(tokenizer):
    sents = tokenizer("toki")
    compare = ["toki"]

    assert sents == compare


@pytest.mark.parametrize("tokenizer", [_sent_tokenize])
def test_unpunct_second_sent(tokenizer):
    sents = tokenizer("mi pona. sina pona")
    compare = ["mi pona.", "sina pona"]
    assert sents == compare


@pytest.mark.parametrize("tokenizer", [_sent_tokenize])
def test_messy_document(tokenizer):
    doc = "nimi mi li jan Wiku...    sina wile seme??!?? mi wile pona tawa jan mute mute a!!! ! !"
    compare = [
        "nimi mi li jan Wiku.",
        ".",
        ".",
        "sina wile seme?",
        "?",
        "!",
        "?",
        "?",
        "mi wile pona tawa jan mute mute a!",
        "!",
        "!",
        "!",
        "!",
    ]
    result = tokenizer(doc)
    assert result == compare


@pytest.mark.parametrize("tokenizer", [_word_tokenize])
def test_sentence_name(tokenizer):
    sent = "nimi mi li jan Wiku."
    compare = ["nimi", "mi", "li", "jan", "Wiku", "."]
    result = tokenizer(sent)
    assert compare == result


@pytest.mark.parametrize("tokenizer", [_word_tokenize])
@pytest.mark.xfail(reason="name joining not implemented")
def test_sentence_long_name(tokenizer):
    sent = "nimi mi li jan Kekan San."
    compare = ["nimi", "mi", "li", "jan", "Kekan San", "."]
    result = tokenizer(sent)
    assert compare == result


@pytest.mark.parametrize("tokenizer", [_word_tokenize])
def test_short_sentence(tokenizer):
    sent = "mi jan Wiku."
    compare = ["mi", "jan", "Wiku", "."]
    result = tokenizer(sent)
    assert compare == result


@pytest.mark.parametrize("tokenizer", [_word_tokenize])
@pytest.mark.xfail(reason="name joining not implemented")
def test_short_sentence_long_name(tokenizer):
    sent = "mi jan Kekan San."
    compare = ["mi", "jan", "Kekan San", "."]
    result = tokenizer(sent)
    assert compare == result


@pytest.mark.parametrize("tokenizer", [_word_tokenize])
@pytest.mark.xfail(reason="number joining not implemented")
def test_nasin_pu_number(tokenizer):
    sent = "mi jo e ilo tu tu wan"
    compare = ["mi", "jo", "e", "ilo", "tu tu wan"]
    result = tokenizer(sent)
    assert compare == result


@pytest.mark.parametrize("tokenizer", [_word_tokenize])
@pytest.mark.xfail(reason="number joining not implemented")
def test_nasin_pu_suli_number(tokenizer):
    sent = "mi jo e ilo tu tu wan"
    compare = ["mi", "jo", "e", "ilo", "mute luka tu"]
    result = tokenizer(sent)
    assert compare == result
