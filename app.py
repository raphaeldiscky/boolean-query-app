from flask import Flask, render_template, request, send_file
import time
import boolean_models
import query_processing

app = Flask(__name__)

# get stopwords from file
stop_words = []
with open("static\stopword-list.txt", "r") as file:
    s = file.read().replace("\n", " ")
stop_words = s.split()

# get inverted index and term doc incidence matrix
dictionary_inverted, docu = boolean_models.inverted_index()
dictionary_term_doc_incidence, docu = boolean_models.term_doc_incidence()

# return relevant document retrieved from inverted index
def documents_ret_inverted_index(a):
    documents = {}
    if a:
        for i in a:
            text = "kompas-" + str(i)
            documents.setdefault(text, [])
            documents[text].append(docu.get(text))
    else:
        documents = {}
    return documents


def remove_item_inside_list(list, item):
    res = [i for i in list if i != item]
    return res


# return relevant document retrieved from term doc incidence matrix
def documents_ret_term_doc_incidence(a):
    documents = {}

    for i in range(0, len(a)):
        if a[i] == 1:
            a.append(i)

    b = remove_item_inside_list(a, 0)
    c = remove_item_inside_list(b, 1)
    a = c
    print(a)

    if a:
        for i in a:
            text = "kompas-" + str(i)
            documents.setdefault(text, [])
            documents[text].append(docu.get(text))
    else:
        documents = {}
    return documents


# ------------------------- app routes ------------------------- #


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/result", methods=["POST"])
def upload():
    start = time.time()
    query = request.form["query"]
    if "$" in query:
        result = query_processing.process_query(query, dictionary_term_doc_incidence)
        documents = documents_ret_term_doc_incidence(result)
    else:
        result = query_processing.process_query(query, dictionary_inverted)
        documents = documents_ret_inverted_index(result)
    end = time.time()
    times = end - start
    return render_template(
        "result.html",
        doc_num=result,
        dictionary=documents,
        len_docs=len(documents),
        time=str(times) + " " + "detik",
    )


@app.route("/static/kompas-docs/<file_name>")
def download_file(file_name):
    path = "static/kompas-docs/" + file_name
    return send_file(path, as_attachment=True)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(405)
def method_not_allowed(e):
    return render_template("405.html"), 405


@app.errorhandler(500)
def method_not_allowed(e):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(debug=True)
