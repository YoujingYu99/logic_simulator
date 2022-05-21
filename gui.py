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
    on_run_button(self, spin_value): Event handler for when the user clicks the run
                                button.
    on_rerun_button(self, spin_value): Event handler for when the user clicks the rerun
    button.
    on_continue_button(self, spin_value): Event handler for when the user clicks the continue
    button.
    get_monitor_names(self): Return monitor_list and monitor_names_list.
    on_monitor_button(self): Event handler for when the user chooses a few monitors and draw the signals on canvas.
    update_monitor(self): Event handler for when the monitor states are updated.
    get_switch_names(self): Return switch_name_list and switch_on_list.
    on_switch_button(self): Event handler for when the user chooses a few switches.
    update_switches(self): Event handler for when the switch state changes
    """

    def __init__(self, title, path, names, devices, network, monitors):
        """Initialise widgets and layout."""
        super().__init__(parent=None, title=title, size=(800, 600))
        self.token = "main_frame"

        # Set input parameters
        self.network = network
        self.names = names
        self.devices = devices
        self.monitors = monitors
        self.style = wx.GetApp().stylesheet
        self.configure_style()

        # Set parameters
        self.cycle_text_colour = (0, 0, 0)
        # Set fonts
        self.cycle_font = wx.Font(
            11, wx.FONTFAMILY_SWISS, 0, 90, underline=False, faceName=""
        )
        self.monitor_font = wx.Font(
            14, wx.FONTFAMILY_ROMAN, 0, 90, underline=False, faceName=""
        )
        self.run_font = wx.Font(
            12, wx.FONTFAMILY_ROMAN, 0, 90, underline=False, faceName=""
        )
        self.console_font = wx.Font(
            12, wx.FONTFAMILY_SWISS, 0, 90, underline=False, faceName=""
        )

        # Monitor names list with two sublists: list of signal monitored and list of signal not monitored
        self.monitor_names_list = []
        self.monitor_list = []
        self.monitor_selected_list = []

        # Switch names and IDs
        # All switch IDs. Only uncomment when other modules ready
        # self.switch_id_list = self.devices.find_devices(self.devices.SWITCH)
        self.switch_id_list = []
        # all switch names
        self.switch_name_list = [self.names.get_name_string(x) for x in self.switch_id_list]
        self.switch_on_list = []

        # Temporarily set file to be not parsed
        self.is_parsed = False


        # configure initial parameters
        self.spin_value = 10
        self.cycles_completed = 0

        # Canvas for drawing signals
        self.canvas = MyGLCanvas(self, devices, monitors, spin_value=self.spin_value)
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
        self.text = CycleNumberText(self, wx.ID_ANY, "Number of Cycles")
        self.text.SetFont(self.cycle_font)
        self.text.SetForegroundColour(wx.Colour(self.cycle_text_colour))
        self.spin = wx.SpinCtrl(
            self,
            wx.ID_ANY,
            str(self.spin_value),
            style=wx.SP_ARROW_KEYS,
            min=0,
            max=100,
        )
        self.run_button = wx.Button(self, wx.ID_ANY, "Run")
        self.continue_button = wx.Button(self, wx.ID_ANY, "Continue")
        self.rerun_button = wx.Button(self, wx.ID_ANY, "Rerun")
        # Monitor and Switch Buttons
        self.monitor_button = wx.Button(self, wx.ID_ANY, "Choose Monitor")
        self.switch_button = wx.Button(self, wx.ID_ANY, "Choose Switch")

        # Set fonts for all
        self.run_button.SetFont(self.run_font)
        self.rerun_button.SetFont(self.run_font)
        self.continue_button.SetFont(self.run_font)
        self.monitor_button.SetFont(self.monitor_font)
        self.switch_button.SetFont(self.monitor_font)

        # self.text_box = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_PROCESS_ENTER)
        # self.console_box = wx.TextCtrl(
        #     self, wx.ID_ANY, self.console_text, style=wx.TE_READONLY | wx.TE_MULTILINE
        # )
        self.console_box = ConsoleBox(
            self, wx.ID_ANY, style=wx.TE_READONLY | wx.TE_MULTILINE
        )
        self.console_box.SetFont(self.console_font)

        # Bind events to widgets
        # self.Bind(wx.EVT_MENU, self.on_menu)
        self.spin.Bind(wx.EVT_SPINCTRL, self.on_spin)
        self.run_button.Bind(wx.EVT_BUTTON, self.on_run_button)
        self.rerun_button.Bind(wx.EVT_BUTTON, self.on_rerun_button)

        ## Uncomment when all modules ready
        # self.continue_button.Bind(wx.EVT_BUTTON, self.on_continue_button())
        # self.monitor_button.Bind(wx.EVT_BUTTON, self.on_monitor_button())
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
        main_sizer.Add(side_sizer, 1, wx.EXPAND | wx.ALL, 5)
        side_sizer.Add(simulation_sizer, 1, wx.EXPAND, 0)
        side_sizer.Add(function_sizer, 1, wx.EXPAND, 0)

        # side sizer configuration
        simulation_setting_sizer.Add(self.text, 1, wx.ALL, 10)
        simulation_setting_sizer.Add(self.spin, 1, wx.ALL, 10)
        simulation_action_sizer.Add(self.run_button, 1, wx.LEFT | wx.RIGHT, 3, 5)
        simulation_action_sizer.Add(self.continue_button, 1, wx.LEFT | wx.RIGHT, 3, 5)
        simulation_action_sizer.Add(self.rerun_button, 1, wx.LEFT | wx.RIGHT, 3, 5)
        simulation_sizer.Add(simulation_setting_sizer, 5, wx.ALL | wx.EXPAND, 5)
        simulation_sizer.Add(simulation_action_sizer, 5, wx.ALL | wx.EXPAND, 5)

        function_sizer.Add(self.monitor_button, 1, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
        function_sizer.Add(self.switch_button, 1, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        # side_sizer.Add(self.text_box, 1, wx.ALL, 5)

        # console sizer configuration
        console_sizer.Add(self.console_box, 5, wx.EXPAND | wx.ALL, 5)
        console_sizer.SetMinSize(self.window_size[0], self.window_size[1] / 3)

        self.SetSizeHints(600, 600)
        # self.SetSizer(main_sizer)
        self.SetSizer(top_level_sizer)

    def configure_style(self):
        self.style.apply_rules(self)

    def on_spin(self, event):
        """Handle the event when the user changes the spin control value."""
        spin_value = self.spin.GetValue()
        text = "".join(["New spin control value: ", str(spin_value)])
        self.canvas.render(text)

    def on_run_button(self, spin_value):
        """Handle the event when the user clicks the run button."""
        # text = "Run button pressed."
        # self.canvas.render(text)
        if self.is_parsed:
            for i in range(spin_value):
                if self.network.execute_network():
                    self.monitors.record_signals()
                else:
                    self.console_box.print_console_message(
                        "Error! Network oscillating."
                    )
                    return False
            self.monitors.display_signals()
            self.canvas.update_monitors(self.monitors)
            return True
        else:
            # Show error if file was not parsed correctly
            text = "Cannot run simulation. Please check your definition file.\n"
            self.console_box.print_console_message(text)

    def on_rerun_button(self, spin_value):
        """Run the simulation from scratch."""
        self.cycles_completed = 0
        if self.is_parsed:

            if spin_value is not None:  # if the number of cycles provided is valid
                self.monitors.reset_monitors()
                self.console_box.print_console_message(
                    "".join(["Running for ", str(spin_value), " cycles"])
                )
                self.devices.cold_startup()
                self.canvas.update_monitors(self.monitors)
                if self.on_run_button(spin_value):
                    self.cycles_completed += spin_value
        else:
            # Show error if file was not parsed correctly
            text = "Cannot rerun simulation. Please check your definition file.\n"
            self.console_box.print_console_message(text)

    def on_continue_button(self):
        """Continue a previously run simulation."""
        if self.is_parsed:
            if self.spin_value is not None:  # if the number of cycles provided is valid
                if self.cycles_completed == 0:
                    self.console_box.print_console_message(
                        "Error! Nothing to continue. Run first."
                    )
                elif self.on_run_button(self.spin_value):
                    self.canvas.update_monitors(self.monitors)
                    self.cycles_completed += self.spin_value
                    self.console_box.print_console_message(
                        " ".join(
                            [
                                "Continuing for",
                                str(self.spin_value),
                                "cycles.",
                                "Total:",
                                str(self.cycles_completed),
                            ]
                        )
                    )
        else:
            # Show error if file was not parsed correctly
            text = "Cannot continue running simulation. Please check your definition file.\n"
            self.console_box.print_console_message(text)

    def get_monitor_names(self):
        """monitor_list : [(device_id, output_id)]
        monitor_names_list :[monitor_name]
        """
        for device in self.devices:
            for output_id, output_signal in device.outputs.items():
                # Append tuple of device_id and output_id, like a monitors dictionary
                # Output id is the port id
                self.monitor_list.append((device.device_id, output_id))
            # Outputs dictionary stores {output_id: output_signal}
            # This returns the name of the signal, which can be monitored
            monitor_name = self.devices.get_signal_name(
                device.device_id, device.port_id
            )
            self.monitor_names_list.append(monitor_name)

    def on_monitor_button(self):
        """Choose signals to monitor and draw."""
        if self.is_parsed:
            # renew the names for monitors
            self.get_monitor_names()
            dlg = wx.MultiChoiceDialog(
                self,
                "Choose the Signals You Wish to Monitor",
                "Monitored Signals",
                self.monitor_names_list,
            )

            # # Set the dialog default before the user sets it
            # dlg.GetSelections(self.monitor_selected_list)

            if dlg.ShowModal() == wx.ID_OK:
                selections = dlg.GetSelections()

                # Set monitors selected by user
                self.monitor_selected_list = selections
                for count in range(len(self.monitor_list)):
                    device_id, output_id = self.monitor_list[count]
                    # If the monitor is selected by user
                    if count in self.monitor_selected_list:
                        # Make monitor
                        monitor_error = self.monitors.make_monitor(
                            device_id, output_id, self.cycles_completed
                        )
                        if monitor_error == self.monitors.NO_ERROR:
                            self.console_box.print_console_message(
                                "Successfully made monitor."
                            )
                        else:
                            self.console_box.print_console_message(
                                "Error! Could not make monitor."
                            )
                self.canvas.draw_signal()
            dlg.Destroy()
        else:
            # Show error if file was not parsed correctly
            text = "Cannot Show on Monitor. Please check your definition file.\n"
            self.console_box.print_console_message(text)

    def update_monitors(self, monitors):
        """Update signals to be monitored and redraw on canvas"""
        self.monitors = monitors
        self.canvas.update_monitors(self.monitors)
        # Re-initialise monitor_list and monitor_names_list
        self.monitor_list = []
        self.monitor_names_list = []
        for device in self.devices:
            for output_id, output_signal in device.outputs.items():
                # Append tuple of device_id and output_id, like a monitors dictionary
                self.monitor_list.append((device.device_id, output_id))
            # Outputs dictionary stores {output_id: output_signal}
            # This returns the name of the signal, which can be monitored
            monitor_name = self.devices.get_signal_name(
                device.device_id, device.port_id
            )
            self.monitor_names_list.append(monitor_name)

        # Re-initialise monitor selections
        self.monitor_selected_list = []
        for count in range(len(self.monitor_list)):
            device_id, output_id = self.monitor_list[count]
            # If signal exists
            if self.monitors.get_monitor_signal((device_id, output_id)) is not None:
                # Add to selected monitor list
                self.monitor_selected_list.append(count)

        self.canvas.update_monitors(self.monitors)

    # def on_zap_monitor(self):
    #     """Remove the specified monitor."""
    #     if self.is_parsed:
    #         monitor = self.read_signal_name()
    #         if monitor is not None:
    #             [device, port] = monitor
    #             if self.monitors.remove_monitor(device, port):
    #                 print("Successfully zapped monitor")
    #             else:
    #                 print("Error! Could not zap monitor.")
    #     else:
    #         # Show error if file was not parsed correctly
    #         text = "Cannot choose a Monitor. Please check your definition file.\n"
    #         self.console_box.print_console_message(text)

    def get_switch_names(self):
        """switch_id_list : list of the switch ids
        switch_names_list : list of switch names
        switch_on_list : list of switch set to High
        """
        # Get switch ids for all devices present
        self.switch_id_list = self.devices.find_devices(self.devices.SWITCH)
        self.switch_name_list = [
            self.names.get_name_string(x) for x in self.switch_id_list
        ]
        for i in range(len(self.switch_id_list)):
            count, switch_id = self.switch_id_list[count]
            if self.devices.get_device(switch_id).switch_state == self.devices.HIGH:
                # Add the position of the switch into the switch_on list
                self.switch_on_list.append(count)

    def on_switch_button(self):
        """Set switch to desired state."""
        if self.is_parsed:
            dlg = wx.MultiChoiceDialog(
                self,
                "Choose the switches to be set to 1",
                "Switch Settings",
                self.switch_name_list,
            )

            # Set the dialogue default before the user chooses it.
            # dlg.SetSelections(self.switch_on_list)

            if dlg.ShowModal() == wx.ID_OK:
                selections = dlg.GetSelections()
                # Update switches
                self.update_switches(selections)

                for count in range(len(selections)):
                    switch_on_list = [self.switch_name_list[x] for x in selections]
                    # switch_off_list = [self.switch_name_list[x] for x in range(
                    #     0, len(self.switch_name_list)) if x not in selections]
                self.switch_on_list = switch_on_list
                self.canvas.draw_signal()
            dlg.Destroy()

        else:
            # Show error if file was not parsed correctly
            text = "Cannot Show on Monitor. Please check your definition file.\n"
            self.console_box.print_console_message(text)

    def update_switches(self, switch_on_list):
        """Update states of the switches and redraw on canvas"""
        # TODO: finish when the names module is ready.
        for indiv_switch in switch_on_list:
            pass

        self.canvas.update_switches(self.devices)


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
        self.token = FileMenu

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

    def configure_style(self):
        self.style.apply_rules(self)

    def print_console_message(self, text):
        """Print text to the console output."""
        self.console_text += text
        self.SetValue(self.console_text)

        # Autoscroll to make last line visible
        pos = self.GetLastPosition()
        self.ShowPosition(pos - 1)

    def clear_console(self):
        """Clear the console output."""
        self.console_text = ""
        self.SetValue(self.console_text)


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
