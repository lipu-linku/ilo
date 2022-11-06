import jasima
templates_books = {"none": "{}",
                   "ku lili": "*{}*",
                   "ku suli": "**{}**",
                   "pu": "***{}***"}
books_order = {"none": 3,
               "ku lili": 2,
               "ku suli": 1,
               "pu": 0}
books_allowed = {"pu": ["pu"],
                 "ku suli": ["pu", "ku suli"],
                 "ku lili": ["pu", "ku suli", "ku lili"],
                 "all": ["pu", "ku suli", "ku lili", "none"]}
def respond(word, book_label):
    data = jasima.bundle["data"]
    data = sorted(data.values(), key=lambda x: books_order[x["book"]])
    responses = {}
    for entry in data:
        if entry["book"] in books_allowed[book_label]:
            w = entry["word"]
            if w[0].lower() not in responses:
                responses[w[0].lower()] = []
            responses[w[0].lower()].append(templates_books[entry["book"].lower()].format(w))
    word = sorted(set(word.lower()))
    response = "\n".join(", ".join(responses[letter]) for letter in word if letter in responses)
    if not response:
        response = "Sorry, but I don't think any toki pona word starts with these characters."
    return response
