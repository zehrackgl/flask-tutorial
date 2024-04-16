from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "This is the home page <h1>Hello<h1>"

@app.route("/search")
def search():
    return "Search Page"

@app.route("/delete/item")
def delete():
    return "Delete Item"

@app.route("/delete/<string:id>")
def delete_item(id):
    return "Id: " + id


if __name__ == "__main__":
    app.run(debug=True)

