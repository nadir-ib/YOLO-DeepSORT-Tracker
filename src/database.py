import sqlite3

class DetectionDatabase:
    def __init__(self, db_path):
        self.connection = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        with self.connection:
            self.connection.execute('''CREATE TABLE IF NOT EXISTS detections (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        object_type TEXT,
                                        timestamp TEXT,
                                        video_path TEXT
                                      )''')

    def insert_detection(self, object_type, timestamp, video_path):
        with self.connection:
            self.connection.execute('''INSERT INTO detections (object_type, timestamp, video_path) 
                                       VALUES (?, ?, ?)''', (object_type, timestamp, video_path))

    def close(self):
        self.connection.close()
