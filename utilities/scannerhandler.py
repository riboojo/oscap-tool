import datetime
import subprocess

class OscapScanner(object):
    def performScan(self):
        current_time = datetime.datetime.now()
        result_filename = f'reports/{current_time}.xml'
        report_filename = f'reports/{current_time}.html'

        subprocess.run(['oscap', 'xccdf', 'eval', '--profile', 'xccdf_org.ssgproject.content_profile_stig', '--results', result_filename, '--report', report_filename, '/usr/share/xml/scap/ssg/content/ssg-firefox-xccdf.xml'])

    def executeFeature(self, command, id_consult=None, id_compare=None):
        if command == 'scan':
            self.performScan()
        elif command == 'history':
            print(f"TODO: print history")
        elif command == 'consult':
            print(f"TODO: print report for #{id_consult}")
        elif command == 'compare':
            print(f"TODO: print comparison between #{id_consult} and #{id_compare}")
        else:
            print(f"{command} is not recognized as a valid command")