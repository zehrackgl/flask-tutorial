from flask import Flask, jsonify, render_template, request, redirect, url_for
import sqlite3


app = Flask(__name__)

# Veritabanı bağlantısı oluşturuyoruz
def connect_db():
    connect = sqlite3.connect('database.db')
    connect.execute('CREATE TABLE IF NOT EXISTS kullanicilar (id INTEGER PRIMARY KEY, isim TEXT, soyisim TEXT, telefon_no TEXT, adres TEXT)')
    return connect

# Ana sayfa, veri ekleme formunu gösterir
@app.route('/veriekle', methods=['GET','POST'])
def veri_ekle():
    if request.method == 'POST':
        print("Received POST request")
        print("Form Data:", request.form)
        connect = connect_db()
        cursor = connect.cursor()
        try:
            cursor.execute("INSERT INTO kullanicilar (isim, soyisim, telefon_no, adres) VALUES (?, ?, ?, ?)",
                           (request.form['isim'], request.form['soyisim'], request.form['telefon_no'], request.form['adres']))
            connect.commit()
            print("Record added successfully")
            # Fetch newly added record
            cursor.execute("SELECT * FROM kullanicilar WHERE rowid = last_insert_rowid()")
            new_record = cursor.fetchone()
            return jsonify({'success': True, 'user': new_record})
        except Exception as e:
            print("Error adding record:", e)
            connect.rollback()
            return jsonify({'success': False, 'message': 'Error adding record'})
        finally:
            connect.close()
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

# Update user route
@app.route('/update/<int:user_id>', methods=['POST'])
def update_user(user_id):
    if request.method == 'POST':
        isim = request.form['isim']
        soyisim = request.form['soyisim']
        telefon = request.form['telefon']
        adres = request.form['adres']
        
        # Update user in database
        connect = connect_db()
        cursor = connect.cursor()
        cursor.execute("UPDATE kullanicilar SET isim=?, soyisim=?, telefon_no=?, adres=? WHERE id=?", (isim, soyisim, telefon, adres, user_id))
        connect.commit()
        connect.close()
        
        return jsonify({'success': True}), 200
    else:
        return 'Method Not Allowed', 405


# Delete user route
@app.route('/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    connect = connect_db()
    cursor = connect.cursor()
    cursor.execute("DELETE FROM kullanicilar WHERE id=?", (user_id,))
    connect.commit()
    connect.close()
    
    
    return jsonify({'success': True}), 200



if __name__ == '__main__':
    app.run(debug=True, port=8080)
