from utilities.scannerhandler import OscapScanner

class OscapArguments(object):
    def printMenu(self):
        print(f"Select one of the following commands:\n1: scan\n2: history\n3: consult\n4: compare")
        selection = input("> ")

        if selection == '1':
            self.executeFeature('scan')
        elif selection == '2':
            self.executeFeature('history')
        elif selection == '3':
            self.printMenuConsult()
        elif selection == '4':
            self.printMenuCompare()
        else:
            print(f"Please enter a valid option")

    def printMenuConsult(self):
        print(f"Enter an ID to consult its report")
        id_consult = input("> ")
        self.executeFeature('consult', id_consult)

    def printMenuCompare(self):
        print(f"Enter the first ID to compare")
        id_consult = input("> ")
        print(f"Enter the second ID to compare")
        id_compare = input("> ")
        self.executeFeature('compare', id_consult, id_compare)

    def executeFeature(self, command, id_consult=None, id_compare=None):
        if command == 'scan':
            scanner = OscapScanner()
            scanner.performScan()
        elif command == 'history':
            print(f"TODO: print history")
        elif command == 'consult':
            print(f"TODO: print report for #{id_consult}")
        elif command == 'compare':
            print(f"TODO: print comparison between #{id_consult} and #{id_compare}")
        else:
            print(f"{command} is not recognized as a valid command")
