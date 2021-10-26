import dictreader
templates_books = {"none": "{}",
                   "ku lili": "*{}*",
                   "ku suli": "**{}**",
                   "pu": "***{}***"}
books_order = {"none": 3,
               "ku lili": 2,
               "ku suli": 1,
               "pu": 0}
books_allowed = {"pu": ["pu"],
                 "kusuli": ["pu", "ku suli"],
                 "ku": ["pu", "ku suli", "ku lili"],
                 "kulili": ["pu", "ku suli", "ku lili"],
                 "ale": ["pu", "ku suli", "ku lili", "none"],
                 "nap": ["pu", "ku suli", "ku lili", "none"]}
def respond(word, include="ale"):
    if include not in books_allowed:
        include = "ale"
    data = dictreader.read_json()
    data = sorted(data, key=lambda x: books_order[x["book"]])
    responses = {}
    for entry in data:
        if entry["book"] in books_allowed[include]:
            w = entry["word"]
            if w[0].lower() not in responses:
                responses[w[0].lower()] = []
            responses[w[0].lower()].append(templates_books[entry["book"].lower()].format(w))
    word = sorted(set(word.lower()))
    response = "\n".join(", ".join(responses[letter]) for letter in word if letter in responses)
    if not response:
        response = "Sorry, but I don't think any toki pona word starts with these characters."
    return response
