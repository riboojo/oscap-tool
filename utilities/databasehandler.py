"""
    OscapDatabase:
        Handle the creation, connections and queries for scans database
"""

import sqlite3
import logging

class OscapDatabase(object):
    """ Handles the interaction with the database """

    QUERY_CREATE_TABLE = '''
        CREATE TABLE IF NOT EXISTS scans (
            scan_id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            result_path TEXT NOT NULL
        )
    '''

    QUERY_ADD_SCAN = 'INSERT INTO scans (timestamp, result_path) VALUES (?, ?)'

    QUERY_GET_SCANS = 'SELECT scan_id, timestamp FROM scans'

    QUERY_GET_REPORT_PATH = 'SELECT result_path FROM scans WHERE scan_id = ?'

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

        self.cursor.execute(self.QUERY_CREATE_TABLE)
        self.connection.commit()

    def add_scan(self, timestamp, result_path):
        """ Function to add a row to the scans table with the provided data """

        self.cursor.execute(self.QUERY_ADD_SCAN, (timestamp, result_path))
        self.connection.commit()

    def get_scans(self):
        """ Function to perform a query of all data found in scans table """

        self.cursor.execute(self.QUERY_GET_SCANS)
        return self.cursor.fetchall()

    def get_report_path(self, scan_id):
        """ Function to perform a query to get the report path of the requested scan id """

        self.cursor.execute(self.QUERY_GET_REPORT_PATH, (scan_id,))
        row = self.cursor.fetchone()
        if row:
            return row[0]
        else:
            return None

    def close(self):
        """ Function to end a connection with the database """

        self.connection.close()
