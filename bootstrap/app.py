from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from markupsafe import Markup

app = Flask(__name__)

# Veritabanı bağlantısı oluşturuyoruz
def connect_db():
    connect = sqlite3.connect('database.db')
    connect.execute('CREATE TABLE IF NOT EXISTS kullanicilar (id INTEGER PRIMARY KEY, isim TEXT, soyisim TEXT, telefon_no TEXT, adres TEXT)')
    return connect

# Ana sayfa, veri ekleme formunu gösterir
@app.route('/veriekle', methods=['GET', 'POST'])
def veri_ekle():
    if request.method == 'POST':
        connect = connect_db()
        cursor = connect.cursor()
        cursor.execute("INSERT INTO kullanicilar (isim, soyisim, telefon_no, adres) VALUES (?, ?, ?, ?)",
                       (request.form['isim'], request.form['soyisim'], request.form['telefon_no'], request.form['adres']))
        connect.commit()
        connect.close()
        return redirect(url_for('anasayfa'))
    return render_template('veriekle.html')

# Anasayfa, daha önce eklenmiş verileri listeler
@app.route('/')
@app.route('/veriler')
def anasayfa():
    connect = connect_db()
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM kullanicilar")
    veriler = cursor.fetchall()
    connect.close()
    return render_template('anasayfa.html', veriler=veriler)

if __name__ == '__main__':
    app.run(debug=True, port=8080)