#!/usr/bin/env python3
"""Parse command line options and arguments for the Logic Simulator.

This script parses options and arguments specified on the command line, and
runs either the command line user interface or the graphical user interface.

Usage
-----
Show help: logsim.py -h
Command line user interface: logsim.py -c <file path>
Graphical user interface: logsim.py <file path>
"""
import getopt
import sys
import logging
import wx

from names import Names
from devices import Devices
from network import Network
from monitors import Monitors
from scanner import Scanner
from parse import Parser
from userint import UserInterface
from gui import Gui
from logic_simulator_app import LogicSimulatorApp

_ = wx.GetTranslation


def main(arg_list):
    """Parse the command line options and arguments specified in arg_list.

    Run either the command line user interface, the graphical user interface,
    or display the usage message.
    """
    usage_message = (
        "Usage:\n"
        "Show help: logsim.py -h\n"
        "Command line user interface: logsim.py -c <file path>\n"
        "Graphical user interface: logsim.py <file path>"
    )
    try:
        options, arguments = getopt.getopt(arg_list, "hc:")
    except getopt.GetoptError:
        print("Error: invalid command line arguments\n")
        print(usage_message)
        sys.exit()

    names = None
    devices = None
    network = None
    monitors = None
    path = None

    # Configure the loggers
    scanner_logger = logging.getLogger("scanner")
    parser_logger = logging.getLogger("parser")
    logging.basicConfig(level=logging.DEBUG)

    for option, path in options:
        if option == "-h":  # print the usage message
            print(usage_message)
            sys.exit()
        elif option == "-c":  # use the command line user interface
            names_instance = Names()
            scanner_instance = Scanner(
                path, names_instance, scanner_logger
            )
            device_instance = Devices(names_instance)
            network_instance = Network(names_instance, device_instance)
            monitor_instance = Monitors(
                names_instance, device_instance, network_instance
            )

            parser = Parser(
                names_instance,
                device_instance,
                network_instance,
                monitor_instance,
                scanner_instance,
                parser_logger,
            )

            if parser.parse_network():
                # Initialise an instance of the userint.UserInterface() class
                names = parser.names
                network = parser.network
                devices = parser.devices
                monitors = parser.monitors
                userint = UserInterface(names, devices, network, monitors)
                userint.command_interface()

    # no options, use GUI
    if not options:

        # if arguments were given
        if arguments:
            print("Error: No input should be given for Graphic "
                  "User Interface\n")
            print(usage_message)
            sys.exit()

        # Initialise an instance of the LogicSimulatorApp class
        app = LogicSimulatorApp('./style.css')
        gui = Gui("Logic Simulator", path, names, devices, network, monitors)
        gui.Show(True)
        app.MainLoop()


if __name__ == "__main__":
    main(sys.argv[1:])
