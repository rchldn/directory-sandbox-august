from flask import Flask, request, jsonify, send_file
import sqlite3
import csv

app = Flask(__name__)

# Helper function to connect to the database
def get_db_connection():
    conn = sqlite3.connect('musicians.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/add-musician', methods=['POST'])
def add_musician():
    data = request.json
    name = data['name']
    genre = data['genre']
    instrument = data['instrument']
    email = data['email']
    
    conn = get_db_connection()
    conn.execute('INSERT INTO musicians (name, genre, instrument, email) VALUES (?, ?, ?, ?)',
                 (name, genre, instrument, email))
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'success'}), 201

@app.route('/export-csv', methods=['GET'])
def export_csv():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM musicians')
    rows = cursor.fetchall()
    conn.close()
    
    with open('musicians_backup.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'name', 'genre', 'instrument', 'email'])
        writer.writerows(rows)
    
    return send_file('musicians_backup.csv', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
