import sqlite3
from datetime import datetime

class DBManager:
    def __init__(self):
        self.conn = sqlite3.connect('db/detections.db')
        self.cursor = self.conn.cursor()
        self.init_db()

    def init_db(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS detections
                              (id INTEGER PRIMARY KEY, objects TEXT, timestamp TEXT)''')
        self.conn.commit()

    def save_detection(self, objects, timestamp):
        self.cursor.execute("INSERT INTO detections (objects, timestamp) VALUES (?, ?)", 
                            (','.join(objects), timestamp))
        self.conn.commit()

    def get_all_records(self):
        self.cursor.execute("SELECT * FROM detections")
        records = self.cursor.fetchall()
        return records  # Return the records for display or further use

    def __del__(self):
        self.conn.close()



if __name__ == "__main__":
    db_manager = DBManager()
    records = db_manager.get_all_records()

    # Display records
    print("ID | Objects Detected | Timestamp | Video Path")
    print("----------------------------------------------------")
    for record in records:
        print(f"{record[0]:<3} | {record[1]:<18} | {record[2]} | {record[3]}")
