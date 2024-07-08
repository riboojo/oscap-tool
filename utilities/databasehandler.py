import sqlite3

class OscapDatabase(object):
    # Constructor for OscapArguments class with default database name
    def __init__(self, db_name=f'database/oscap_scans_history.db'):
        self.dbname = db_name

    # Function to start a connection with the database
    def open(self):
        self.connection = sqlite3.connect(self.dbname)
        self.cursor = self.connection.cursor()
        self.createTable()

    # Function to create the scans table containing the scan id, timestamp, result/report paths
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

    # Function to add a row to the scans table with the provided data
    def addScan(self, timestamp, report_path, result_path):
        self.cursor.execute('INSERT INTO scans (timestamp, result_path, report_path) VALUES (?, ?, ?)', (timestamp, result_path, report_path))
        self.connection.commit()

    # Function to perform a query of all data found in scans table
    def getScans(self):
        self.cursor.execute('SELECT scan_id, timestamp FROM scans')
        return self.cursor.fetchall()

    # Function to perform a query to get the report path of the requested scan id
    def getReportPath(self, scan_id):
        self.cursor.execute('SELECT report_path FROM scans WHERE scan_id = ?', (scan_id,))
        row = self.cursor.fetchone()
        if row:
            return row[0]
        else:
            return None

    # Function to end a connection with the database
    def close(self):
        self.connection.close()
