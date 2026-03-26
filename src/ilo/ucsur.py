import re
from typing import cast

from ilo.cog_utils import load_file

vocab = cast(dict[str, str], load_file(__file__, "ucsur.json"))
chars = list(map(re.escape, list(vocab.keys())))
chars.sort(key=len, reverse=True)


def ucsur_replace(string: str):
    string = clean_string(string)
    response = re.sub(
        "|".join(chars),
        lambda x: (
            vocab[x.group(0)] + " "
            if vocab[x.group(0)][0] in "abcdefghijklmnopqrstuvwxyz"
            else vocab[x.group(0)]
        ),
        string,
    )  # the ternary adds a space after any latin word, which ucsur characters don't tend to have in-between

    # cleaning up:
    response = " ".join(response.split(" "))  # collapse all spaces to one
    response = re.sub(
        r"\u0020(?=[,\.:!\?\]\)<v\^>\+\-\&=_\|\}12345678　」])", "", response
    )
    response = re.sub("\u0020(?=([　-〿]|[︀-️]|[󱤀-󱧿]|[←-↙]))", "", response)

    return response


def clean_string(string: str):
    clean_string = re.findall(r"([ -~]|[　-〿]|[︀-️]|[󱤀-󱧿]|[←-↙])", string)
    clean_string = "".join(clean_string)
    return clean_string
