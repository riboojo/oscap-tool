"""
    OscapScanner:
        Handle the four functionality of the OscapTool: scan, history, consult and compare
"""

import datetime
import subprocess
from utilities.databasehandler import OscapDatabase
from utilities.reportshandler import OscapReports

class OscapScanner(object):
    """ Handle the four functionality of the tool """

    def __init__(self):
        """ Constructor for OscapScanner class """

        self.db = OscapDatabase()
        self.reports = OscapReports()

    def perform_scan(self):
        """ Function to run the oscap command and save the results data into the database """

        current_time = datetime.datetime.now()
        result_filename = f'reports/{current_time}.xml'
        report_filename = f'reports/{current_time}.html'

        # Run the oscap command with stig profile and ssg-ol8-xccdf
        subprocess.run(['oscap', 'xccdf', 'eval', '--profile', 'xccdf_org.ssgproject.content_profile_stig', '--results', result_filename, '--report', report_filename, '/usr/share/xml/scap/ssg/content/ssg-ol8-xccdf.xml'], check=False)

        # Start database connection, perform query and clos connection
        self.db.open()
        self.db.add_scan(current_time, result_filename, report_filename)
        self.db.close()

    def read_history(self):
        """ Function to retrieve the scans history """

        # Start database connection, perform query and clos connection
        self.db.open()
        all_scans = self.db.get_scans()
        self.db.close()

        if all_scans:
            for scan_id, timestamp in all_scans:
                print(f'ID #{scan_id} generated on {timestamp}')
        else:
            print('There are no entries in the history database')

    def consult_report(self, id_consult):
        """ Function to print the requested scan report """

        # Start database connection, perform query and clos connection
        self.db.open()
        report_path = self.db.get_report_path(id_consult)
        self.db.close()

        if report_path:
            # Get the summarized data from .xml report
            summary, _, results = self.reports.parse_xml(report_path, id_consult)
            # Print the requested report in a cool format
            self.reports.print_report(summary, results)
        else:
            print(f'There is no ID #{id_consult} in the history database')

    def compare_reports(self, id_consult, id_compare):
        """ Function to compare a couple of requested scans reports """

        self.db.open()
        report_path = self.db.get_report_path(id_consult)
        compare_path = self.db.get_report_path(id_compare)
        self.db.close()

        if report_path and compare_path:
            # Get the summarized data from both .xml report
            _, overall1, results1 = self.reports.parse_xml(report_path, id_consult)
            _, overall2, results2 = self.reports.parse_xml(compare_path, id_compare)
            differences = self.reports.compare_results(results1, results2)

            # Print the differences of the requested reports in a cool format
            self.reports.print_differences(overall1, overall2, differences)
        else:
            print('Invalid ID given as parameters')

    def execute_feature(self, command, id_consult=None, id_compare=None):
        """ Function to determine which functionality has been requested """

        if command == 'scan':
            self.perform_scan()
        elif command == 'history':
            self.read_history()
        elif command == 'consult':
            self.consult_report(id_consult)
        elif command == 'compare':
            self.compare_reports(id_consult, id_compare)
        else:
            print(f"{command} is not recognized as a valid command")
