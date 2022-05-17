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
        self.OnInit()

    def OnInit(self):
        # # only uncomment when full code integratable
        # names = Names()
        # devices = Devices(names)
        # network = Network(names, devices)
        # monitors = Monitors(names, devices, network)

        names = None
        devices = None
        network = None
        monitors = None
        path = None


        """Initialise variables."""
        self.names = names
        self.devices = devices
        self.monitors = monitors
        self.network = network

        return True





