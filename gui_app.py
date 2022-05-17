import wx
from gui import Gui
import builtins
from names import Names
from devices import Devices
from network import Network
from monitors import Monitors

# create App class
class LogicSimulatorApp(wx.App):
    def __init__(self):
        super().__init__()
        self.InitBrowser()

    def InitBrowser(self):
        """Initialise variables."""
        self.names = names
        self.devices = devices
        self.monitors = monitors
        self.network = network


