"""
    OscapArguments:
        Handle the parsing of arguments next to oscaptool execution or print a menu if none provided
"""

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

        # Add the optional arguments to the parser
        parser.add_argument('command', type=str, nargs='?', default=None, help='Select one of the following options: scan, history, consult, compare')
        parser.add_argument('id_consult', type=str, nargs='?', default=None, help='Select a valid ID (you can execute -history command to retrieve valid IDs)')
        parser.add_argument('id_compare', type=str, nargs='?', default=None, help='Select a valid ID (you can execute -history command to retrieve valid IDs)')

        args = parser.parse_args()
        command = args.command
        id_consult = args.id_consult
        id_compare = args.id_compare

        if not command:
            # If no arguments given then print the menu
            self.print_menu()
        elif command=='consult' and not id_consult:
            # If no IDs given then print the consult menu
            self.print_menu_consult()
        elif command=='compare' and not id_compare:
            # If no IDs given then print the compare menu
            self.print_menu_compare()
        else:
            self.scanner.execute_feature(command, id_consult, id_compare)

    def print_menu(self):
        """ Function to print the main menu in case no arguments given """

        print("Select one of the following commands:\n1: scan\n2: history\n3: consult\n4: compare")
        selection = input("> ")

        if selection == '1':
            self.scanner.execute_feature('scan')
        elif selection == '2':
            self.scanner.execute_feature('history')
        elif selection == '3':
            self.print_menu_consult()
        elif selection == '4':
            self.print_menu_compare()
        else:
            print("Please enter a valid option")

    def print_menu_consult(self):
        """ Function to print the consult menu in case no id given """

        print("Enter an ID to consult its report")
        id_consult = input("> ")
        self.scanner.execute_feature('consult', id_consult)

    def print_menu_compare(self):
        """ Function to print the compare menu in case no id given """

        print("Enter the first ID to compare")
        id_consult = input("> ")
        print("Enter the second ID to compare")
        id_compare = input("> ")
        self.scanner.execute_feature('compare', id_consult, id_compare)
