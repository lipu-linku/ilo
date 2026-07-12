from ilo import data

templates_books = {
    "none": "{}",
    "ku lili": "*{}*",
    "ku suli": "**{}**",
    "pu": "***{}***",
}
books_order = {"none": 3, "ku lili": 2, "ku suli": 1, "pu": 0}
books_allowed = {
    "pu": ["pu"],
    "ku suli": ["pu", "ku suli"],
    "ku lili": ["pu", "ku suli", "ku lili"],
    "all": ["pu", "ku suli", "ku lili", "none"],
}


def respond(text: str, book_label):
    """
    return a dictionary mapping single letters to the list of words starting with that letter
    """
    fetched = sorted(data.get_non_sandbox_words().values(), key=lambda word: books_order[word.book])
    responses = {}
    for entry in fetched:
        if entry.book in books_allowed[book_label]:
            char = entry.string[0].lower()
            if char not in responses:
                responses[char] = []
            responses[char].append(
                templates_books[entry.book.lower()].format(entry.string)
            )
    text = sorted(set(text.lower()))
    response = "\n".join(
        ", ".join(responses[letter]) for letter in text if letter in responses
    )
    if not response:
        response = (
            "Sorry, but I don't think any toki pona word starts with these characters."
        )
    return response
