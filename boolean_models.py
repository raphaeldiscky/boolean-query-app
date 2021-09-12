import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


def inverted_index():
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

        # lowercase and remove stopwords
        set_stop_words = set(stopwords.words("indonesian"))
        s = s.lower()
        s = [words if words not in set_stop_words else "" for words in s.split(" ")]
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


def term_doc_incidence():
    dictionary = {}
    documents = {}
    docs = []

    exclist = string.punctuation + string.digits
    translator = str.maketrans(exclist, " " * len(exclist))

    for i in range(0, 50):
        doc_no = i
        with open("static\kompas-docs\kompas-" + str(doc_no) + ".txt", "r") as file:
            next(file)
            s = file.read().replace("\n", " ").translate(translator).lower()
            docs.append(s)

        key = "kompas-" + str(doc_no)
        documents.setdefault(key, [])
        documents[key].append(s)  # {'kompas-0': [''], 'kompas-1': ['']}

    # tokenize and stop words
    for i in docs:
        text_tokens = word_tokenize(i)
        set_stop_words = set(stopwords.words("indonesian"))
        unique_terms = {word for word in text_tokens if not word in set_stop_words}

        # construct term-doc incidence matrix
        for term in unique_terms:
            dictionary[term] = []

            for doc in docs:
                if term in doc:
                    dictionary[term].append(1)
                else:
                    dictionary[term].append(0)
    return dictionary, documents
