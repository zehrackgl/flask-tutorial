from flask import Flask, render_template, request, redirect, url_for 

app = Flask(__name__)


@app.route("/")
def page():
    return render_template("index3.html")

@app.route("/toplam", methods = ["GET","POST"])
def toplam():
    if request.method == "POST":
        number1 = request.form.get("number1")
        number2 = request.form.get("number2")
        return render_template("number.html", total = int(number1) + int(number2))
    else:
        return redirect(url_for("page"))


if __name__ == "__main__":
    app.run(debug= True, port= 8008)