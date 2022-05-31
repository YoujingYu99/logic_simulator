import wx
import os
from names import Names
from devices import Devices
from network import Network
from monitors import Monitors
from scanner import Scanner
from parse import Parser

"""Define the graphical user interface elements for the Logic Simulator.
Used in the Gui class to enable the user to perform functions and view console output
Classes:
--------
FileMenu - handles all menu items under 'File' menu
HelpMenu - handles all menu items under 'Help' menu
AboutMenu - handles all menu items under 'About' menu
ConsoleBox - handles all console items in which the user views the messages
"""


class FileMenu(wx.Menu):
    """This class contains all the methods for creating the menu named 'File'
    Public methods
    --------------
    on_init(self): Initialisation step
    on_open(self, event): Open definition file.
    on_save_trace(self, event): Save a screenshot of the canvas as picture.
    on_save_console(self, event): Save the console output to a text file.
    on_quit(self, event): Quit system.
    """

    def __init__(self, parentFrame, main_canvas):
        super().__init__()
        self.on_init()
        self.parentFrame = parentFrame
        self.canvas = main_canvas
        self.token = "FileMenu"

    def on_init(self):
        """Initialise menu and menu items"""
        # menu stuff hoes here
        # add new item
        # special command : wx.ID_NEW is for buttons that create new items or new windows
        # text has text and shortcut command
        # newItem = wx.MenuItem(
        #     parentMenu=self, id=wx.ID_NEW, text="&New\tCtrl+N", kind=wx.ITEM_NORMAL
        # )

        # open an item
        openItem = wx.MenuItem(
            parentMenu=self, id=wx.ID_OPEN, text="&Open\tCtrl+O", kind=wx.ITEM_NORMAL
        )
        self.Append(openItem)
        self.Bind(wx.EVT_MENU, handler=self.on_open, source=openItem)
        self.AppendSeparator()

        saveTraceItem = wx.MenuItem(
            parentMenu=self,
            id=wx.ID_ANY,
            text="&Save Trace\tCtrl+S",
            helpString="Save the Trace",
            kind=wx.ITEM_NORMAL,
        )
        self.Append(saveTraceItem)
        self.Bind(wx.EVT_MENU, handler=self.on_save_trace, source=saveTraceItem)

        saveConsoleItem = wx.MenuItem(
            parentMenu=self,
            id=wx.ID_ANY,
            text="&Save Console\tCtrl+C",
            helpString="Save the Console Output",
            kind=wx.ITEM_NORMAL,
        )
        self.Append(saveConsoleItem)
        self.Bind(wx.EVT_MENU, handler=self.on_save_console, source=saveConsoleItem)

        self.AppendSeparator()

        # quit project
        quitItem = wx.MenuItem(parentMenu=self, id=wx.ID_EXIT, text="&Quit\tCtrl+Q")
        self.Append(quitItem)
        self.Bind(wx.EVT_MENU, handler=self.on_quit, source=quitItem)

    # open definition file(text file at the moment)
    def on_open(self, event):
        """Open definition file uploaded by user."""
        wildcard = "TXT files (*.txt)|*.txt"
        dialog = wx.FileDialog(
            self.parentFrame,
            "Open Text Files",
            wildcard=wildcard,
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
        )
        if dialog.ShowModal() == wx.ID_CANCEL:
            return None

        path = dialog.GetPath()
        if os.path.exists(path):
            with open(path) as myfile:
                text = "Loading {file_name:}.".format(file_name=path)
                self.parentFrame.console_box.print_console_message(text)

                names = Names()
                devices = Devices(names)
                network = Network(names, devices)
                monitors = Monitors(names, devices, network)
                scanner = Scanner(myfile, names)
                parser = Parser(names, devices, network, monitors, scanner)
                if parser.parse_network():
                    # Set successfully parsed
                    self.parentFrame.is_parsed = True
                    # update names, networks etc modules
                    self.parentFrame.names = names
                    self.parentFrame.network = network
                    self.parentFrames.devices = devices
                    self.parentFrame.monitors = monitors
                else:
                    self.parentFrame.console_box.print_console_message(
                        text="File cannot be parsed. Please check your definition file."
                    )

        dialog.Destroy()

    # possibly save file in the future
    def on_save_trace(self, event=None):
        """Save screenshot of the App."""
        im = self.get_screenshot()
        save_dialog = wx.FileDialog(
            self.parentFrame,
            "Save file as ...",
            defaultFile="",
            wildcard=".png",
            style=wx.FD_SAVE,
        )
        # GetPath fails to get actual path
        # save_dialog.ShowModal()
        # import pdb; pdb.set_trace()
        if save_dialog.ShowModal() == wx.ID_OK:
            path = save_dialog.GetPath()
            if not (path[-4:].lower() == ".png"):
                path = path + ".png"
            im.SaveFile(path)

    def get_screenshot(self):
        """Capture a screenshot of the App."""
        screen = wx.WindowDC(self.canvas)
        size = self.canvas.GetSize()
        width = size.width
        height = size.height
        bmp = wx.Bitmap(width, height)
        # import pdb; pdb.set_trace()

        # Create a memory DC that will be used for actually taking the screenshot
        memDC = wx.MemoryDC()
        # Tell the memory DC to use our Bitmap
        # all drawing action on the memory DC will go to the Bitmap now
        memDC.SelectObject(bmp)
        # Blit (in this case copy) the actual screen on the memory DC
        memDC.Blit(0, 0, width, height, screen, 0, 0)
        # Select the Bitmap out of the memory DC by selecting a new bitmap
        memDC.SelectObject(wx.NullBitmap)
        im = bmp.ConvertToImage()
        return im

    def on_save_console(self, event=None):
        """Capture the console messages in one txt file."""
        dialog = wx.FileDialog(
            self.parentFrame,
            "Save your console output",
            defaultFile="",
            wildcard=".txt",
            style=wx.FD_SAVE,
        )

        if dialog.ShowModal() == wx.ID_CANCEL:
            return None
        path = dialog.GetPath()
        data = self.parentFrame.console_box.all_console_messages()
        with open(path, "w+") as myfile:
            for line in data:
                myfile.write(str(line) + "\n")

    def on_quit(self, event):
        """Quit the system."""
        self.parentFrame.Close()


class HelpMenu(wx.Menu):
    """This class contains all the methods for creating the menu named 'Help'
    Public methods
    --------------
    on_init(self): Initialisation step
    on_info(self, event): Display Help information.
    on_documentation(self, event): Direct to documentation page of the App.
    """

    def __init__(self, parentFrame):
        super().__init__()
        self.on_init()
        self.parentFrame = parentFrame

    def on_init(self):
        """Initialise menu and menu items"""
        # menu stuff hoes here

        # open an item
        infoItem = wx.MenuItem(parentMenu=self, id=wx.ID_INFO, text="&Start\tCtrl+H")
        self.Append(infoItem)
        self.Bind(wx.EVT_MENU, handler=self.on_info, source=infoItem)
        self.AppendSeparator()

        # about information on project
        documentationItem = wx.MenuItem(
            parentMenu=self, id=wx.ID_ANY, text="&Documetation\tCtrl+D"
        )
        self.Append(documentationItem)
        self.Bind(wx.EVT_MENU, handler=self.on_documentation, source=documentationItem)

    def on_info(self, event):
        """Display Basic Help information"""
        wx.MessageBox(
            "Start by uploading your definition file by selecting 'File/Open'.\nChoose the number of cycles you wish "
            "to run by spinning the button.Then press 'Run' to run the simulation.\nClick on 'Choose Monitor' or "
            "'Choose Switch' to choose the signals to be displayed or state of switches.",
            "How to Use Logic Simulator App",
            wx.ICON_INFORMATION | wx.OK,
        )
        return

    def on_documentation(self, event):
        """Open the GitHub Page"""
        wx.LaunchDefaultBrowser("https://github.com/LogicSimulator/GF2_11")


class AboutMenu(wx.Menu):
    """This class contains all the methods for creating the menu named 'About'
    Public methods
    --------------
    on_init(self): Initialisation step
    on_about(self, event): Display About information.
    """

    def __init__(self, parentFrame):
        super().__init__()
        self.on_init()
        self.parentFrame = parentFrame

    def on_init(self):
        """Initialise menu and menu items"""
        # menu stuff hoes here

        # about information on project
        aboutItem = wx.MenuItem(parentMenu=self, id=wx.ID_ABOUT, text="&About\tCtrl+A")
        self.Append(aboutItem)
        self.Bind(wx.EVT_MENU, handler=self.on_about, source=aboutItem)

    def on_about(self, event):
        """Display about information"""
        wx.MessageBox(
            "Logic Simulator created by Mojisola Agboola\n2017\nDeveloped and completed by Niko, Youjing and Gleb, "
            "the most brilliant engineers of the 2019 cohort.",
            "About Logsim",
            wx.ICON_INFORMATION | wx.OK,
        )
        return


class ConsoleBox(wx.TextCtrl):
    """This class contains all the methods for creating the menu named 'File'
    Public methods
    --------------
    on_init(self): Initialisation step
    configure_style(self): Follow the stylesheet defined.
    print_console_message(self, event): Print user message to console.
    clear_console(self, event): Clear all console outputs.
    all_console_messages(self): Return all console messages in list.
    """

    def __init__(
        self,
        parent,
        id=wx.ID_ANY,
        label="",
        pos=wx.DefaultPosition,
        size=wx.DefaultSize,
        style=0,
    ):
        super(ConsoleBox, self).__init__(parent, id, label, pos, size, style)
        self.token = "console_box"
        if parent:
            self.token = parent.token + self.token
        self.style = wx.GetApp().stylesheet
        self.configure_style()
        self.console_text = ""
        # Initialise a console log that contains all console messages
        self.console_log = []

    def configure_style(self):
        """Configure the CSS stylesheet in the element"""
        self.style.apply_rules(self)

    def print_console_message(self, input_text, clear=False):
        """Print text to the console output."""
        if clear:
            self.console_text = input_text
        else:
            self.console_text += input_text
        self.SetValue(self.console_text)
        self.console_log.append(self.console_text)

        # Autoscroll to make last line visible
        pos = self.GetLastPosition()
        self.ShowPosition(pos - 1)

    def clear_console(self):
        """Clear the console output."""
        self.console_text = "New simulation!\n"
        self.print_console_message(input_text=self.console_text, clear=True)

    def all_console_messages(self):
        """Keep all console messages in list"""
        return self.console_log


class CycleNumberText(wx.StaticText):
    """This class contains all the methods for displaying the static number of cycles
    Public methods
    --------------
    configure_style(self): Follow the stylesheet defined.
    """

    def __init__(
        self,
        parent,
        id=wx.ID_ANY,
        label="",
        pos=wx.DefaultPosition,
        size=wx.DefaultSize,
        style=0,
        name=wx.StaticTextNameStr,
    ):
        super(CycleNumberText, self).__init__(parent, id, label, pos, size, style, name)
        self.token = "cycle_text"
        if parent:
            self.token = parent.token + self.token
        self.style = wx.GetApp().stylesheet
        self.configure_style()

    def configure_style(self):
        """Configure the CSS stylesheet in the element"""
        self.style.apply_rules(self)
