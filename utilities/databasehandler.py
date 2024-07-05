import sqlite3

class OscapDatabase(object):
    def __init__(self, db_name=f'database/oscap_scans_history.db'):
        self.dbname = db_name

    def open(self):
        self.connection = sqlite3.connect(self.dbname)
        self.cursor = self.connection.cursor()
        self.createTable()

    def createTable(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS scans (
                scan_id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                result_path TEXT NOT NULL,
                report_path TEXT NOT NULL
            )
        ''')
        self.connection.commit()

    def addScan(self, timestamp, report_path, result_path):
        self.cursor.execute('INSERT INTO scans (timestamp, result_path, report_path) VALUES (?, ?, ?)', (timestamp, result_path, report_path))
        self.connection.commit()

    def getScans(self):
        self.cursor.execute('SELECT scan_id, timestamp FROM scans')
        return self.cursor.fetchall()

    def getReportPath(self, scan_id):
        self.cursor.execute('SELECT report_path FROM scans WHERE scan_id = ?', (scan_id,))
        row = self.cursor.fetchone()
        if row:
            return row[0]
        else:
            return None

    def close(self):
        self.connection.close()
