from flask import Flask, render_template, request, send_file
import time
import boolean_models
import query_processing

app = Flask(__name__)

# get stopwords from file
stop_words = []
with open("stopword-list.txt", "r") as file:
    s = file.read().replace("\n", " ")
stop_words = s.split()

# get inverted_index
dictionary_inverted, docu = boolean_models.inverted_index(stop_words)


# return relevant document retrieved
def documents_ret(a):
    documents = {}
    if a:
        for i in a:
            text = "kompas-" + str(i)
            documents.setdefault(text, [])
            documents[text].append(docu.get(text))
    else:
        documents = {}
    return documents


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/result", methods=["POST"])
def upload():
    start = time.time()
    query = request.form["query"]
    result = query_processing.process_query(query, dictionary_inverted)
    documents = documents_ret(result)
    end = time.time()
    times = end - start
    return render_template(
        "result.html",
        doc_num=result,
        dictionary=documents,
        len_docs=len(documents),
        time=str(times) + " " + "detik",
    )


@app.route("/kompas-docs/<file_name>")
def download_file(file_name):
    path = "kompas-docs/" + file_name
    return send_file(path, as_attachment=True)


@app.errorhandler(404)
def page_not_found():
    return render_template("404.html"), 404


@app.errorhandler(405)
def method_not_allowed():
    return render_template("405.html"), 405


if __name__ == "__main__":
    app.run()
