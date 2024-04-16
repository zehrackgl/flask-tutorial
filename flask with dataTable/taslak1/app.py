from flask import Flask, render_template, jsonify, request
import sqlite3
import json

app = Flask(__name__)

def connect_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # This allows column access by name
    return conn

@app.route("/veriekle", methods=['GET', 'POST'])
def veri_ekle():
    if request.method == 'POST':
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO kullanicilar (isim, soyisim, telefon_no, adres) VALUES (?, ?, ?, ?)",
                   (request.form['isim'], request.form['soyisim'], request.form['telefon_no'], request.form['adres']))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('veriekle.html')

@app.route("/")
@app.route("/veriler")
def anasayfa():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM kullanicilar")
    rows = cur.fetchall()
    my_data = [list(row) for row in rows]
    my_cols = [{'title': col[0]} for col in cur.description]  # Using column headers directly from the cursor
    conn.close()
    return render_template('anasayfa.html', my_data=json.dumps(my_data), my_cols=json.dumps(my_cols))

if __name__ == '__main__':
    app.run(debug=True, port=8080)
