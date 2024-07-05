from utilities.scannerhandler import OscapScanner
import argparse

class OscapArguments(object):
    def __init__(self):
        self.scanner = OscapScanner()

    def start(self):
        parser = argparse.ArgumentParser(description='Simple command line tool for regular openscap scans')

        parser.add_argument('command', type=str, nargs='?', default=None, help='Select one of the following options: scan, history, consult, compare')
        parser.add_argument('id_consult', type=str, nargs='?', default=None, help='Select a valid ID (you can execute -history command to retrieve valid IDs)')
        parser.add_argument('id_compare', type=str, nargs='?', default=None, help='Select a valid ID (you can execute -history command to retrieve valid IDs)')

        args = parser.parse_args()
        command = args.command
        id_consult = args.id_consult
        id_compare = args.id_compare

        if not command:
            self.printMenu()
        elif command=='consult' and not id_consult:
            self.printMenuConsult()
        elif command=='compare' and not id_compare:
            self.printMenuCompare()
        else:
            scanner = OscapScanner()
            scanner.executeFeature(command, id_consult, id_compare)

    def printMenu(self):
        print(f"Select one of the following commands:\n1: scan\n2: history\n3: consult\n4: compare")
        selection = input("> ")

        if selection == '1':
            self.scanner.executeFeature('scan')
        elif selection == '2':
            self.scanner.executeFeature('history')
        elif selection == '3':
            self.printMenuConsult()
        elif selection == '4':
            self.printMenuCompare()
        else:
            print(f"Please enter a valid option")

    def printMenuConsult(self):
        print(f"Enter an ID to consult its report")
        id_consult = input("> ")
        self.scanner.executeFeature('consult', id_consult)

    def printMenuCompare(self):
        print(f"Enter the first ID to compare")
        id_consult = input("> ")
        print(f"Enter the second ID to compare")
        id_compare = input("> ")
        self.scanner.executeFeature('compare', id_consult, id_compare)
