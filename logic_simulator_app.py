"""Initialise the Logic Simulator App.

This script initialises the LogicSimulatorApp instance using wx.App instance.

Classes
-----
LogicSimulatorApp: Creates user interface for logic simulation.
"""

import wx
import stylesheet
from pathlib import Path

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

        

        # Chinese = 45
        SUPPORTED_LANGS_INTS = [wx.LANGUAGE_CHINESE_SIMPLIFIED, wx.LANGUAGE_ENGLISH]
        
        system_lang = wx.Locale.GetSystemLanguage()
        
        system_lang = wx.LANGUAGE_CHINESE_SIMPLIFIED
        if system_lang in SUPPORTED_LANGS_INTS:
            app_lang = system_lang
        else:
            app_lang = wx.LANGUAGE_ENGLISH
            

        wx.Locale.AddCatalogLookupPathPrefix(
            str(Path(__file__).resolve().with_name("locale"))
        )
        self.locale = wx.Locale()
        self.locale.Init(app_lang)

        if self.locale.IsOk():
            self.locale.AddCatalog("I18Nwxapp")
        else:
            self.locale = None
            print('FATAL ERROR: failed to initialise wx.Locale.')

        return True

