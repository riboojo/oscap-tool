"""
    OscapArguments:
        Handle the parsing of arguments next to oscaptool execution or print a menu if none provided
"""

import logging
import argparse
from utilities.scannerhandler import OscapScanner

class OscapArguments(object):
    """ Handles the parsing of arguments """

    def __init__(self):
        """ Constructor for OscapArguments class """

        # Instantiate an OscapScanner to handle main functionality
        self.scanner = OscapScanner()

    def start(self):
        """ Function to start the arguments parser and handle if arguments were given or not """

        parser = argparse.ArgumentParser(description='Simple command line tool for regular openscap scans')

        # Add a subparser for the requested command
        subparsers = parser.add_subparsers(dest='command', help='Select one of the following options: scan, history, consult, compare')

        # Handle the scan command subparser
        scan_parser = subparsers.add_parser('scan', help='Perform a oscap scan based on provided xccdf file and profile')
        scan_parser.add_argument('-x', '--xccdf', type=str, default='ssg-ol8-xccdf.xml', help='Select a valid a XCCDF filename (you can look for them inside /usr/share/xml/scap/ssg/content/)')
        scan_parser.add_argument('-p', '--profile', type=str, default='xccdf_org.ssgproject.content_profile_stig', help='Select a valid profile')

        # Handle the history command subparser
        subparsers.add_parser('history', help='Print history table of saved scans')

        # Handle the consult command subparser
        consult_parser = subparsers.add_parser('consult', help='Consult a saved scan report by its ID')
        consult_parser.add_argument('-f', '--frm', type=int, required=True, help='Select a valid ID (you can execute -history command to retrieve valid IDs)')

        # Handle the compare command subparser
        compare_parser = subparsers.add_parser('compare', help='Compare two saved scan reports by their IDs')
        compare_parser.add_argument('-f', '--frm', type=int, required=True, help='Select a valid ID (you can execute -history command to retrieve valid IDs)')
        compare_parser.add_argument('-t', '--to', type=int, required=True, help='Select a valid ID (you can execute -history command to retrieve valid IDs)')

        # Add an argument for log level configuration
        parser.add_argument('-l', '--loglevel', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], default='INFO', help='Provide a logging level')

        # Get the entered arguments
        args = parser.parse_args()

        # Set the logging configuration
        logging.basicConfig(level=args.loglevel, format= '[%(asctime)s] {%(module)s:%(lineno)d} %(levelname)s - %(message)s', datefmt='%H:%M:%S')

        if not args.command:
            logging.error(f"Please enter a valid command, check --help menu for correct tool handling")
        else:
            validated_args = self.validate_args(args)
            self.scanner.execute_feature(**validated_args)

    def validate_args(self, args):
        validated_args = {
            'command': args.command,
        }

        if hasattr(args, 'xccdf'):
            validated_args['xccdf'] = args.xccdf

        if hasattr(args, 'profile'):
            validated_args['profile'] = args.profile

        if hasattr(args, 'frm'):
            validated_args['frm'] = args.frm

        if hasattr(args, 'to'):
            validated_args['to'] = args.to

        return validated_args

        

