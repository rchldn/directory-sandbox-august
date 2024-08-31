from flask import Flask, request, jsonify, render_template_string
import sqlite3
import csv
import threading
import time
import os
#import requests


app = Flask(__name__)


# response = requests.get('https://api.example.com/data')  # Ensure this URL is correct
# try:
#     response.raise_for_status()  # Raise an exception for HTTP errors
#     data = response.json()  # Attempt to parse JSON
#     print(data)
# except requests.exceptions.HTTPError as err:
#     print(f"HTTP error occurred: {err}")
# except ValueError as err:
#     print(f"Error parsing JSON: {err}")
# except Exception as err:
#     print(f"An unexpected error occurred: {err}")

# Database file path
DB_FILE_PATH = 'musicians.db'
# Path to the CSV file
CSV_FILE_PATH = 'musicians_backup.csv'

# Helper function to connect to the database
def get_db_connection():
    conn = sqlite3.connect('musicians.db')
    conn.row_factory = sqlite3.Row
    return conn

def update_csv():
    while True:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM musicians')
        rows = cursor.fetchall()
        conn.close()
        
        # Ensure the directory exists if CSV file is inside a folder
        os.makedirs(os.path.dirname(CSV_FILE_PATH), exist_ok=True)

        with open(CSV_FILE_PATH, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'name', 'genre', 'instrument', 'email'])
            writer.writerows(rows)
        
        # Wait for 1 hour before updating again (commented out bc this might interfere with automatic updates down below)
       #  time.sleep(3600)

@app.route('/data')
def data():
    return jsonify({"key": "value"})  # Ensure you're sending JSON


@app.route('/test', methods=['GET'])
def test_route():
    return "Test route is working!"

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

        # Update CSV file immediately after inserting data
    update_csv()
    
    return jsonify({'status': 'success'}), 201

def backup_database(source_db, backup_db):
    # Connect to the source database
    conn = sqlite3.connect(source_db)
    # Create a backup connection to the new file
    with sqlite3.connect(backup_db) as backup_conn:
        # Perform the backup
        conn.backup(backup_conn)
    print(f'Backup of {source_db} completed to {backup_db}.')

    # New route for searching musicians
@app.route('/search', methods=['GET'])
def search_musician():
    genre = request.args.get('genre')
    instrument = request.args.get('instrument')

    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT name, genre, instrument, email FROM musicians WHERE genre = ? AND instrument = ?"
    cursor.execute(query, (genre, instrument))
    results = cursor.fetchall()
    conn.close()

    # Convert results to a list of dictionaries
    musicians = []
    for row in results:
        musicians.append({
            'name': row['name'],
            'genre': row['genre'],
            'instrument': row['instrument'],
            'email': row['email']
        })

    return jsonify(musicians)


if __name__ == '__main__':
    # Optionally, start a background task for periodic updates
    # threading.Thread(target=update_csv, daemon=True).start()
    backup_database('form_data.db', 'form_data_backup.db')
    app.runapp.run(host='127.0.0.1', port=5500, debug=True)