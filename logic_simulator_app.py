import wx
from gui import Gui
import builtins
# import stylesheet
from names import Names
from devices import Devices
from network import Network
from monitors import Monitors


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
        # self.stylesheet = stylesheet.WXStyleSheet(css_file)

    def on_init(self):
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


        return True





