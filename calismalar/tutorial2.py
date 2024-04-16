from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def page():
    message = "Bu bir mesajdır..."
    numbers= [1, 2, 3, 4, 5, 6, 7]
    return render_template("index2.html", message = message, numbers = numbers)




if __name__ == "__main__":
    app.run(debug= True, port= 8000)