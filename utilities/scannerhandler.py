import datetime
import subprocess

class OscapScanner(object):
    def performScan(self):
        current_time = datetime.datetime.now()
        report_filename = f'reports/{current_time}.xml'

        subprocess.run(['oscap', 'xccdf', 'eval', '--profile', 'xccdf_org.ssgproject.content_profile_stig', '--results', report_filename, '/usr/share/xml/scap/ssg/content/ssg-firefox-xccdf.xml'])

