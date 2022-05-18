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

        # set FileMenu
        fileMenu = FileMenu(parentFrame=self)
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")

        # set menubar
        self.SetMenuBar(menuBar)

        # Canvas for drawing signals
        self.canvas = MyGLCanvas(self, devices, monitors)
        # Get window size
        self.window_size = self.GetClientSize()

        # Configure console properties
        self.console_text = "Welcom to Logic Simulation App!"

        # Configure the widgets
        self.text = wx.StaticText(self, wx.ID_ANY, "Cycles")
        self.spin = wx.SpinCtrl(self, wx.ID_ANY, "10")
        self.run_button = wx.Button(self, wx.ID_ANY, "Run")
        self.text_box = wx.TextCtrl(self, wx.ID_ANY, "",
                                    style=wx.TE_PROCESS_ENTER)
        self.console_box = wx.TextCtrl(self, wx.ID_ANY, self.console_text,
                                          style=wx.TE_READONLY |
                                                wx.TE_MULTILINE)

        # Bind events to widgets
        # self.Bind(wx.EVT_MENU, self.on_menu)
        self.spin.Bind(wx.EVT_SPINCTRL, self.on_spin)
        self.run_button.Bind(wx.EVT_BUTTON, self.on_run_button)
        self.text_box.Bind(wx.EVT_TEXT_ENTER, self.on_text_box)

        # Configure sizers for layout
        top_level_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        side_sizer = wx.BoxSizer(wx.VERTICAL)
        console_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Box.Add(control, proportion, flag, border)
        top_level_sizer.Add(main_sizer, 5, wx.ALL | wx.EXPAND, 5)
        top_level_sizer.Add(console_sizer, 2, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(self.canvas, 5, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(side_sizer, 1, wx.ALL, 5)


        # side sizer configuration
        side_sizer.Add(self.text, 1, wx.TOP, 10)
        side_sizer.Add(self.spin, 1, wx.ALL, 5)
        side_sizer.Add(self.run_button, 1, wx.ALL, 5)
        side_sizer.Add(self.text_box, 1, wx.ALL, 5)

        # console sizer configuration
        console_sizer.Add(self.console_box, 5, wx.EXPAND | wx.ALL, 5)
        console_sizer.SetMinSize(self.window_size[0], self.window_size[1]/3)

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
        self.console_box.ShowPosition(pos-1)

    def clear_console(self):
        """Clear the console output."""
        self.console_text = ""
        self.console_box.SetValue(self.console_text)


class FileMenu(wx.Menu):
    """This class contains all the methods for creating the menu named 'File'
        Public methods
        --------------
        on_init(self): Initialisation step
        onOpen(self, event): Open definition file.
        on_about(self, event): Display about information.
        on_quit(self, event): Quit system.
    """

    def __init__(self, parentFrame):
        super().__init__()
        self.on_init()
        self.parentFrame = parentFrame

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
        self.Bind(wx.EVT_MENU, handler=self.onOpen, source=openItem)
        self.AppendSeparator()

        # saveItem = wx.MenuItem(
        #     parentMenu=self,
        #     id=wx.ID_SAVE,
        #     text="&Save\tCtrl+S",
        #     helpString="Save your file",
        #     kind=wx.ITEM_NORMAL,
        # )
        # self.Append(saveItem)
        # self.Bind(wx.EVT_MENU, handler=self.onSave, source=saveItem)

        # about information on project
        aboutItem = wx.MenuItem(parentMenu=self, id=wx.ID_ABOUT, text="&About\tCtrl+A")
        self.Append(aboutItem)
        self.Bind(wx.EVT_MENU, handler=self.on_about, source=aboutItem)
        self.AppendSeparator()

        # quit project
        quitItem = wx.MenuItem(parentMenu=self, id=wx.ID_EXIT, text="&Quit\tCtrl+Q")
        self.Append(quitItem)
        self.Bind(wx.EVT_MENU, handler=self.on_quit, source=quitItem)
        self.AppendSeparator()

    # open definition file(text file at the moment)
    def onOpen(self, event):
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
    # def onSave(self, event):
    #     dialog = wx.FileDialog(
    #         self.parentFrame,
    #         message="Save your data",
    #         defaultFile="Untitled.txt",
    #         style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
    #     )
    #
    #     if dialog.ShowModal() == wx.ID_CANCEL:
    #         return None
    #
    #     path = dialog.GetPath()
    #     data = self.parentFrame.text.GetValue()
    #     print(data)
    #     data = data.split("\n")
    #     print(data)
    #     with open(path, "w+") as myfile:
    #         for line in data:
    #             myfile.write(line + "\n")

    def on_about(self, event):
        """Display about information"""
        wx.MessageBox("Logic Simulator\nCreated by Mojisola Agboola\n2017",
                      "About Logsim", wx.ICON_INFORMATION | wx.OK)
        return

    def on_quit(self, event):
        """Quit the system."""
        self.parentFrame.Close()


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