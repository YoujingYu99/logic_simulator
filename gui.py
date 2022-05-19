"""Implement the graphical user interface for the Logic Simulator.
Used in the Logic Simulator project to enable the user to run the simulation
or adjust the network properties.
Classes:
--------
Gui - configures the main window and all the widgets.
FileMenu - handles all menu items under 'File' menu
"""
import os
import wx
from wx import html2

from names import Names
from devices import Devices
from network import Network
from monitors import Monitors
from scanner import Scanner
from parse import Parser
from gl_canvas import MyGLCanvas


class Gui(wx.Frame):
    """Configure the main window and all the widgets.
    This class provides a graphical user interface for the Logic Simulator and
    enables the user to change the circuit properties and run simulations.
    Parameters
    ----------
    title: title of the window.
    Public methods
    --------------
    on_menu(self, event): Event handler for the file menu.
    on_spin(self, event): Event handler for when the user changes the spin
                           control value.
    on_run_button(self, event): Event handler for when the user clicks the run
                                button.
    on_text_box(self, event): Event handler for when the user enters text.
    """

    def __init__(self, title, path, names, devices, network, monitors):
        """Initialise widgets and layout."""
        super().__init__(parent=None, title=title, size=(800, 600))

        # Canvas for drawing signals
        self.canvas = MyGLCanvas(self, devices, monitors)
        # Get window size
        self.window_size = self.GetClientSize()

        # Set FileMenu
        fileMenu = FileMenu(parentFrame=self, main_canvas=self.canvas)
        # Set HelpMenu
        helpMenu = HelpMenu(parentFrame=self)
        # Set AboutMenu
        aboutMenu = AboutMenu(parentFrame=self)
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")
        menuBar.Append(aboutMenu, "&About")

        # Set menubar
        self.SetMenuBar(menuBar)

        # Configure console properties
        self.console_text = "Welcome to Logic Simulation App!"

        # Configure the widgets
        self.text = wx.StaticText(self, wx.ID_ANY, "Number of Cycles")
        self.spin = wx.SpinCtrl(self, wx.ID_ANY, "10")
        self.run_button = wx.Button(self, wx.ID_ANY, "Run")
        self.stop_button = wx.Button(self, wx.ID_ANY, "Stop")
        self.rerun_button = wx.Button(self, wx.ID_ANY, "Rerun")
        self.monitor_button = wx.Button(self, wx.ID_ANY, "Choose Monitor")
        self.switch_button = wx.Button(self, wx.ID_ANY, "Choose Switch")
        # self.text_box = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_PROCESS_ENTER)
        self.console_box = wx.TextCtrl(
            self, wx.ID_ANY, self.console_text, style=wx.TE_READONLY | wx.TE_MULTILINE
        )

        # Bind events to widgets
        # self.Bind(wx.EVT_MENU, self.on_menu)
        self.spin.Bind(wx.EVT_SPINCTRL, self.on_spin)
        self.run_button.Bind(wx.EVT_BUTTON, self.on_run_button)
        # self.text_box.Bind(wx.EVT_TEXT_ENTER, self.on_text_box)

        ## Configure sizers for layout
        # Controls the entire screen
        top_level_sizer = wx.BoxSizer(wx.VERTICAL)
        # Contains canvas and sidebar
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # Contains simulation/function sizers
        side_sizer = wx.BoxSizer(wx.VERTICAL)
        # Contains the console
        console_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Sidebar Sizers
        simulation_sizer = wx.StaticBoxSizer(wx.VERTICAL, self)
        simulation_setting_sizer = wx.BoxSizer(wx.HORIZONTAL)
        simulation_action_sizer = wx.BoxSizer(wx.HORIZONTAL)
        function_sizer = wx.StaticBoxSizer(wx.VERTICAL, self)


        # Box.Add(control, proportion, flag, border)
        top_level_sizer.Add(main_sizer, 5, wx.ALL | wx.EXPAND, 5)
        top_level_sizer.Add(console_sizer, 2, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(self.canvas, 5, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(side_sizer, 5, wx.EXPAND |wx.ALL, 5)
        side_sizer.Add(simulation_sizer, 1, wx.EXPAND, 0)
        side_sizer.Add(function_sizer, 1, wx.EXPAND, 0)

        # side sizer configuration
        simulation_setting_sizer.Add(self.text, 1, wx.TOP, 10)
        simulation_setting_sizer.Add(self.spin, 1, wx.TOP, 5)
        simulation_action_sizer.Add(self.run_button, 1, wx.LEFT | wx.RIGHT, 3, 5)
        simulation_action_sizer.Add(self.stop_button, 1, wx.LEFT | wx.RIGHT, 3, 5)
        simulation_action_sizer.Add(self.rerun_button, 1, wx.LEFT | wx.RIGHT, 3, 5)
        simulation_sizer.Add(simulation_setting_sizer, 5, wx.ALL | wx.EXPAND, 5)
        simulation_sizer.Add(simulation_action_sizer, 5, wx.ALL | wx.EXPAND, 5)

        function_sizer.Add(self.monitor_button, 1, wx.EXPAND | wx.TOP | wx.BOTTOM, 5 )
        function_sizer.Add(self.switch_button, 1, wx.EXPAND | wx.TOP | wx.BOTTOM, 5 )

        # side_sizer.Add(self.text_box, 1, wx.ALL, 5)

        # console sizer configuration
        console_sizer.Add(self.console_box, 5, wx.EXPAND | wx.ALL, 5)
        console_sizer.SetMinSize(self.window_size[0], self.window_size[1] / 3)

        self.SetSizeHints(600, 600)
        # self.SetSizer(main_sizer)
        self.SetSizer(top_level_sizer)

    def on_spin(self, event):
        """Handle the event when the user changes the spin control value."""
        spin_value = self.spin.GetValue()
        text = "".join(["New spin control value: ", str(spin_value)])
        self.canvas.render(text)

    def on_run_button(self, event):
        """Handle the event when the user clicks the run button."""
        text = "Run button pressed."
        self.canvas.render(text)

    def on_text_box(self, event):
        """Handle the event when the user enters text."""
        text_box_value = self.text_box.GetValue()
        text = "".join(["New text box value: ", text_box_value])
        self.canvas.render(text)

    def print_to_console(self, text):
        """Print text to the console output."""
        self.console_text += text
        self.console_box.SetValue(self.console_text)

        # Autoscroll to make last line visible
        pos = self.console_box.GetLastPosition()
        self.console_box.ShowPosition(pos - 1)

    def clear_console(self):
        """Clear the console output."""
        self.console_text = ""
        self.console_box.SetValue(self.console_text)


class FileMenu(wx.Menu):
    """This class contains all the methods for creating the menu named 'File'
    Public methods
    --------------
    on_init(self): Initialisation step
    on_open(self, event): Open definition file.
    on_save(self, event): Save a screenshot of the whole window.
    on_quit(self, event): Quit system.
    """

    def __init__(self, parentFrame, main_canvas):
        super().__init__()
        self.on_init()
        self.parentFrame = parentFrame
        self.canvas = main_canvas

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

        saveItem = wx.MenuItem(
            parentMenu=self,
            id=wx.ID_SAVE,
            text="&Save\tCtrl+S",
            helpString="Save your file",
            kind=wx.ITEM_NORMAL,
        )
        self.Append(saveItem)
        self.Bind(wx.EVT_MENU, handler=self.on_save, source=saveItem)

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
                for line in myfile:
                    self.parentFrame.text.WriteText(line)

        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPath()
            text = "Loading definition file:  " + str(path) + "\n"

        dialog.Destroy()

    # possibly save file in the future
    def on_save(self, event=None):
        """Save screenshot of the App."""
        im = self.get_screenshot()
        save_dialog = wx.FileDialog(
            self.parentFrame,
            "Save file as ...",
            defaultFile="",
            wildcard="*.png",
            style=wx.FD_SAVE
        )
        # GetPath fails to get actual path
        path = save_dialog.GetPath()
        if save_dialog.ShowModal() == wx.ID_OK:
            if not (path[-4:].lower() == ".png"):
                path = path + ".png"
                im.SaveFile(path)

    def get_screenshot(self):
        """Capture a screenshot of the App."""
        screen = wx.ScreenDC()

        size = screen.GetSize()
        width = size.width
        height = size.height
        bmp = wx.Bitmap(width, height)

        # Create a memory DC that will be used for actually taking the screenshot
        memDC = wx.MemoryDC()
        # Tell the memory DC to use our Bitmap
        # all drawing action on the memory DC will go to the Bitmap now
        memDC.SelectObject(bmp)
        # Blit (in this case copy) the actual screen on the memory DC
        memDC.Blit(
            0, 0,
            width, height,
            screen,
            0, 0
        )
        # Select the Bitmap out of the memory DC by selecting a new bitmap
        memDC.SelectObject(wx.NullBitmap)
        im = bmp.ConvertToImage()
        return im

    # def on_save(self, event):
    #     context = wx.ClientDC(self.main_panel)
    #     memory = wx.MemoryDC()
    #     x, y = self.client_size
    #     bitmap = wx.EmptyBitmap(x, y, -1)
    #     memory.SelectObject(bitmap)
    #     memory.Blit(0, 0, x, y, context, 0, 0)
    #     memory.SelectObject(wx.NullBitmap)
    #     bitmap.SaveFile('test.bmp', wx.BITMAP_TYPE_BMP)
    # # def on_save(self, event):
    #
    #     # based largely on code posted to wxpython-users by Andrea Gavana 2006-11-08
    #     size = dcSource.Size
    #
    #     # Create a Bitmap that will later on hold the screenshot image
    #     # Note that the Bitmap must have a size big enough to hold the screenshot
    #     # -1 means using the current default colour depth
    #     bmp = wx.EmptyBitmap(size.width, size.height)
    #
    #     # Create a memory DC that will be used for actually taking the screenshot
    #     memDC = wx.MemoryDC()
    #
    #     # Tell the memory DC to use our Bitmap
    #     # all drawing action on the memory DC will go to the Bitmap now
    #     memDC.SelectObject(bmp)
    #
    #     # Blit (in this case copy) the actual screen on the memory DC
    #     # and thus the Bitmap
    #     memDC.Blit(0,  # Copy to this X coordinate
    #                0,  # Copy to this Y coordinate
    #                size.width,  # Copy this width
    #                size.height,  # Copy this height
    #                dcSource,  # From where do we copy?
    #                0,  # What's the X offset in the original DC?
    #                0  # What's the Y offset in the original DC?
    #                )
    #
    #     # Select the Bitmap out of the memory DC by selecting a new
    #     # uninitialized Bitmap
    #     memDC.SelectObject(wx.NullBitmap)
    #
    #     img = bmp.ConvertToImage()
    #     img.SaveFile('saved.png', wx.BITMAP_TYPE_PNG)
    # dialog = wx.FileDialog(
    #     self.parentFrame,
    #     message="Save your data",
    #     defaultFile="Untitled.txt",
    #     style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
    # )
    #
    # if dialog.ShowModal() == wx.ID_CANCEL:
    #     return None
    #
    # path = dialog.GetPath()
    # data = self.parentFrame.text.GetValue()
    # print(data)
    # data = data.split("\n")
    # print(data)
    # with open(path, "w+") as myfile:
    #     for line in data:
    #         myfile.write(line + "\n")

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
        infoItem = wx.MenuItem(parentMenu=self, id=wx.ID_INFO, text="&Open\tCtrl+H")
        self.Append(infoItem)
        self.Bind(wx.EVT_MENU, handler=self.on_info, source=infoItem)
        self.AppendSeparator()

        # about information on project
        documentationItem = wx.MenuItem(
            parentMenu=self, id=wx.ID_ANY, text="&Documetation\tCtrl+A"
        )
        self.Append(documentationItem)
        self.Bind(wx.EVT_MENU, handler=self.on_documentation, source=documentationItem)
        self.AppendSeparator()

    def on_info(self, event):
        """Display Basic Help information"""
        wx.MessageBox(
            "Start by uploading your definition file by selecting 'File/Open'. Then press 'Run' to run the simulation.",
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
        self.AppendSeparator()

    def on_about(self, event):
        """Display about information"""
        wx.MessageBox(
            "Logic Simulator\nCreated by Mojisola Agboola\n2017",
            "About Logsim",
            wx.ICON_INFORMATION | wx.OK,
        )
        return

# class ConsolePanel(wx.Panel):
#     """This class contains all the methods for creating the console panel.
#         Public methods
#         --------------
#         on_init(self): Initialisation step.
#         print_to_console(self, text): Print text to console.
#         clear_console(self): Clear all console outputs.
#     """
#
#     def __init__(self, parentFrame):
#         wx.Panel.__init__(self, parent=parentFrame)
#         # print welcome text
#         welcome_text = 'Welcome to Logic Simulator!'
#         self.console_text = welcome_text
#         self.console_box = wx.TextCtrl(self, wx.ID_ANY, self.console_text,
#                            style=wx.TE_READONLY |
#                                  wx.TE_MULTILINE)
#
#     def on_init(self):
#         """Initialise Console Message"""
#         # print welcome text
#         self.print_to_console(text=self.console_text)
#
#     def print_to_console(self, text):
#         """Print text to the console output."""
#         self.console_text += text
#         self.console_box.SetValue(self.console_text)
#
#         # Autoscroll to make last line visible
#         pos = self.console_box.GetLastPosition()
#         self.console_box.ShowPosition(pos-1)
#
#     def clear_console(self):
#         """Clear the console output."""
#         self.console_text = ""
#         self.console_box.SetValue(self.console_text)
