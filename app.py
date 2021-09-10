from flask import Flask, render_template
import boolean_models

app = Flask(__name__)


@app.route("/")
def dictionary():
    result = boolean_models.function(4)
    return render_template("home.html", result=result)


if __name__ == "__main__":
    app.run()
