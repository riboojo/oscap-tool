import datetime
import subprocess
from utilities.databasehandler import OscapDatabase
from utilities.reportshandler import OscapReports

class OscapScanner(object):
    # Constructor for OscapScanner class
    def __init__(self):
        self.db = OscapDatabase()
        self.reports = OscapReports()

    # Function to run the oscap command and save the results data into the database
    def performScan(self):
        current_time = datetime.datetime.now()
        result_filename = f'reports/{current_time}.xml'
        report_filename = f'reports/{current_time}.html'

        # Run the oscap command with stig profile and ssg-ol8-xccdf
        subprocess.run(['oscap', 'xccdf', 'eval', '--profile', 'xccdf_org.ssgproject.content_profile_stig', '--results', result_filename, '--report', report_filename, '/usr/share/xml/scap/ssg/content/ssg-ol8-xccdf.xml'])

        # Start database connection, perform query and clos connection
        self.db.open()
        self.db.addScan(current_time, result_filename, report_filename)
        self.db.close()

    # Function to retrieve the scans history
    def readHistory(self):
        # Start database connection, perform query and clos connection
        self.db.open()
        allScans = self.db.getScans()
        self.db.close()

        if allScans:
            for scan_id, timestamp in allScans:
                print(f'ID #{scan_id} generated on {timestamp}')
        else:
            print(f'There are no entries in the history database')

    # Function to print the requested scan report
    def consultReport(self, id_consult):
        # Start database connection, perform query and clos connection
        self.db.open()
        report_path = self.db.getReportPath(id_consult)
        self.db.close()

        if report_path:
            # Get the summarized data from .xml report
            summary, overall, results = self.reports.parse_xml(report_path, id_consult)
            # Print the requested report in a cool format
            self.reports.print_report(summary, results)
        else:
            print(f'There is no ID #{id_consult} in the history database')

    # Function to compare a couple of requested scans reports
    def compareReports(self, id_consult, id_compare):
        self.db.open()
        report_path = self.db.getReportPath(id_consult)
        compare_path = self.db.getReportPath(id_compare)
        self.db.close()

        if report_path and compare_path:
            # Get the summarized data from both .xml report
            summary1, overall1, results1 = self.reports.parse_xml(report_path, id_consult)
            summary2, overall2, results2 = self.reports.parse_xml(compare_path, id_compare)
            differences = self.reports.compare_reports(results1, results2)

            # Print the differences of the requested reports in a cool format
            self.reports.print_differences(overall1, overall2, differences)
        else:
            print(f'Invalid ID given as parameters')

    # Function to determine which functionality has been requested
    def executeFeature(self, command, id_consult=None, id_compare=None):
        if command == 'scan':
            self.performScan()
        elif command == 'history':
            self.readHistory()
        elif command == 'consult':
            self.consultReport(id_consult)
        elif command == 'compare':
            self.compareReports(id_consult, id_compare)
        else:
            print(f"{command} is not recognized as a valid command")
