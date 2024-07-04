import datetime
import subprocess

class OscapScanner(object):
    def performScan(self):
        current_time = datetime.datetime.now()
        result_filename = f'reports/{current_time}.xml'
        report_filename = f'reports/{current_time}.html'

        subprocess.run(['oscap', 'xccdf', 'eval', '--profile', 'xccdf_org.ssgproject.content_profile_stig', '--results', result_filename, '--report', report_filename, '/usr/share/xml/scap/ssg/content/ssg-firefox-xccdf.xml'])
