"""
    OscapDatabase:
        Handle the creation, connections and queries for scans database
"""

import sqlite3

class OscapDatabase(object):
    """ handles the interaction with the database """

    def __init__(self, db_name='database/oscap_scans_history.db'):
        """ Constructor for OscapArguments class with default database name """

        self.dbname = db_name
        self.connection = None
        self.cursor = None

    def open(self):
        """ Function to start a connection with the database """

        self.connection = sqlite3.connect(self.dbname)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        """ Function to create the scans table containing the scan id, timestamp, result/report paths """

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS scans (
                scan_id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                result_path TEXT NOT NULL,
                report_path TEXT NOT NULL
            )
        ''')
        self.connection.commit()

    def add_scan(self, timestamp, report_path, result_path):
        """ Function to add a row to the scans table with the provided data """

        self.cursor.execute('INSERT INTO scans (timestamp, result_path, report_path) VALUES (?, ?, ?)', (timestamp, result_path, report_path))
        self.connection.commit()

    def get_scans(self):
        """ Function to perform a query of all data found in scans table """

        self.cursor.execute('SELECT scan_id, timestamp FROM scans')
        return self.cursor.fetchall()

    def get_report_path(self, scan_id):
        """ Function to perform a query to get the report path of the requested scan id """

        self.cursor.execute('SELECT report_path FROM scans WHERE scan_id = ?', (scan_id,))
        row = self.cursor.fetchone()
        if row:
            return row[0]
        else:
            return None

    def close(self):
        """ Function to end a connection with the database """

        self.connection.close()
