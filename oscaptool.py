from utilities.argumentshandler import OscapArguments
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Simple command line tool for regular openscap scans')

    parser.add_argument('command', type=str, nargs='?', default=None, help='Select one of the following options: scan, history, consult, compare')
    parser.add_argument('id_consult', type=str, nargs='?', default=None, help='Select a valid ID (you can execute -history command to retrieve valid IDs)')
    parser.add_argument('id_compare', type=str, nargs='?', default=None, help='Select a valid ID (you can execute -history command to retrieve valid IDs)')

    args = parser.parse_args()
    command = args.command
    id_consult = args.id_consult
    id_compare = args.id_compare

    arghandler = OscapArguments()

    if not command:
        arghandler.printMenu()
    elif command=='consult' and not id_consult:
        arghandler.printMenuConsult()
    elif command=='compare' and not id_compare:
        arghandler.printMenuCompare()
    else:
        arghandler.executeFeature(command, id_consult, id_compare)