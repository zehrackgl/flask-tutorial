from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from markupsafe import Markup

app = Flask(__name__)

def connect_db():
    connect = sqlite3.connect('database.db')
    connect.execute('CREATE TABLE IF NOT EXISTS kullanicilar (id INTEGER PRIMARY KEY, isim TEXT, soyisim TEXT, telefon_no TEXT, adres TEXT)')
    return connect

@app.route('/')
def page():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    connect = connect_db()
    cursor = connect.cursor()
    cursor.execute("INSERT INTO kullanicilar (isim, soyisim, telefon_no, adres) VALUES (?, ?, ?, ?)",
                   (request.form['isim'], request.form['soyisim'], request.form['telefon_no'], request.form['adres']))
    connect.commit()
    connect.close()
    return redirect(url_for('page'))

if __name__ == '__main__':
    app.run(debug=True)

