from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = "caircocoders-ednalan"

DATABASE = 'testingdb.sqlite'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/ajaxlivesearch", methods=["POST", "GET"])
def ajaxlivesearch():
    conn = get_db_connection()
    cur = conn.cursor()
    employee = []
    numrows = 0
    if request.method == 'POST':
        search_word = request.form['query']
        print(search_word)
        if search_word == '':
            query = "SELECT * from employee ORDER BY id"
            cur.execute(query)
            employee = cur.fetchall()
        else:
            search_word = f"%{search_word}%"
            query = "SELECT * FROM employee WHERE name LIKE ? OR email LIKE ? OR phone LIKE ? ORDER BY id DESC LIMIT 20"
            cur.execute(query, (search_word, search_word, search_word))
            employee = cur.fetchall()
            numrows = len(employee)
            print(numrows)
    conn.close()
    return jsonify({'htmlresponse': render_template('response.html', employee=employee, numrows=numrows)})

if __name__ == "__main__":
    app.run()
