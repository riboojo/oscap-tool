"""
    Main script to execute the OscalTool
"""

from utilities.argumentshandler import OscapArguments

if __name__ == '__main__':
    # Instantiate an OscapArguments to handle the input argumments of the command
    arghandler = OscapArguments()
    arghandler.start()
