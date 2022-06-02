"""Initialise the Logic Simulator App.

This script initialises the LogicSimulatorApp instance using wx.App instance.

Classes
-----
LogicSimulatorApp: Creates user interface for logic simulation.
"""

import wx
import stylesheet


# create App class
class LogicSimulatorApp(wx.App):
    """This class creates a LogicSimulatorApp of the type wx.App.

    --------------
    Public methods
    --------------
    on_init(self, event): Initialisation with all parsed information
    passed into the App.
    """

    def __init__(self, css_file):
        """Initialise properties."""
        super().__init__()
        self.on_init()
        self.stylesheet = stylesheet.WXStyleSheet(css_file)

    def on_init(self):
        """Initialise the app when called."""
        return True
