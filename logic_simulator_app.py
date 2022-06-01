import wx
from gui import Gui
import builtins
import logging
import stylesheet
from names import Names
from devices import Devices
from network import Network
from monitors import Monitors
from scanner import Scanner
from parse import Parser


# create App class
class LogicSimulatorApp(wx.App):
    """This class creates a LogicSimulatorApp of the type wx.App.
    --------------
    Public methods
    --------------
    on_init(self, event): Initialisation with all parsed information passed into the App.
    """
    def __init__(self, css_file):
        super().__init__()
        self.on_init()
        self.stylesheet = stylesheet.WXStyleSheet(css_file)

    def on_init(self):

        return True





