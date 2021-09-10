import string


def inverted_index(stop_words):
    dictionary = {}
    documents = {}

    exclist = string.punctuation + string.digits
    translator = str.maketrans(exclist, " " * len(exclist))

    for i in range(0, 50):
        doc_no = i
        with open("static\kompas-docs\kompas-" + str(doc_no) + ".txt", "r") as file:
            next(file)
            s = file.read().replace("\n", " ").translate(translator)

        key = "kompas-" + str(doc_no)
        documents.setdefault(key, [])
        documents[key].append(s)

        # lowecase and remove stopwords
        s = s.lower()
        s = [words if words not in stop_words else "" for words in s.split(" ")]
        doc = []
        doc = list(filter(None, s))

        # create posting list
        for x in doc:
            key = x
            dictionary.setdefault(key, [])
            dictionary[key].append(doc_no)

        # remove duplicates
        dictionary = {a: list(set(b)) for a, b in dictionary.items()}
    return dictionary, documents
