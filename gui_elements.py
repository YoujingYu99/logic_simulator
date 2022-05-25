import wx
import os


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
                for line in myfile:
                    self.parentFrame.text.WriteText(line)

        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPath()
            text = "Loading definition file:  " + str(path) + "\n"

        dialog.Destroy()

    # possibly save file in the future
    def on_save_trace(self, event=None):
        """Save screenshot of the App."""
        im = self.get_screenshot()
        save_dialog = wx.FileDialog(
            self.parentFrame,
            "Save file as ...",
            defaultFile="",
            wildcard="*.png",
            style=wx.FD_SAVE,
        )
        # GetPath fails to get actual path
        path = save_dialog.GetPath()
        if save_dialog.ShowModal() == wx.ID_OK:
            if not (path[-4:].lower() == ".png"):
                path = path + ".png"
                im.SaveFile(path)

    def get_screenshot(self):
        """Capture a screenshot of the App."""
        # TODO: not working atm
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
        memDC.Blit(0, 0, width, height, screen, 0, 0)
        # Select the Bitmap out of the memory DC by selecting a new bitmap
        memDC.SelectObject(wx.NullBitmap)
        im = bmp.ConvertToImage()
        return im

    def on_save_console(self, event=None):
        """ Capture the console messages in one txt file."""
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
        self.style.apply_rules(self)
