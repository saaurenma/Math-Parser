from flask import Flask, request, render_template, flash,redirect,url_for
from parsing import evaluation

app = Flask(__name__)


@app.errorhandler(500)
def internal_server_error(e):
    flash("An internal server error has occurred. Please try again later.", "danger")
    return redirect(url_for('home.html'))


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    expression = None
    if request.method == "POST":
        expression = request.form["expression"]
        result = evaluation(expression)
    return render_template("home.html", result=result, expression=expression)


if __name__ == '__main__':
    app.run(debug=True)
    app.run()
