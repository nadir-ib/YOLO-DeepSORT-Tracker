from flask import Flask, render_template
import sqlite3
import os

app = Flask(__name__)

# Path to the SQLite database
DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'db', 'detections.db')
print(DATABASE_PATH)

def get_database_records():
    """Retrieve records from the database."""
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT object_type, timestamp, video_path FROM detections")
    records = cursor.fetchall()
    connection.close()
    return records

@app.route('/')
def index():
    # Fetch records from the database
    records = get_database_records()
    return render_template('index.html', records=records)

if __name__ == '__main__':
    app.run(debug=True)
