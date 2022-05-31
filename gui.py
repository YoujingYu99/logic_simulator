"""Implement the graphical user interface for the Logic Simulator.
Used in the Logic Simulator project to enable the user to run the simulation
or adjust the network properties.
Classes:
--------
Gui - configures the main window and all the widgets.
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
from gui_elements import FileMenu, HelpMenu, AboutMenu, ConsoleBox, CycleNumberText


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
        # self.style = wx.GetApp().stylesheet
        # self.configure_style()

        # Set parameters
        self.cycle_text_colour = (0, 0, 0)
        # Set fonts
        self.cycle_font = wx.Font(
            11, wx.FONTFAMILY_DEFAULT, 0, weight=90, underline=False, faceName=""
        )
        self.monitor_font = wx.Font(
            14, wx.FONTFAMILY_DEFAULT, 0, weight=90, underline=False, faceName=""
        )
        self.run_font = wx.Font(
            12, wx.FONTFAMILY_DEFAULT, 0, weight=90, underline=False, faceName=""
        )
        self.console_font = wx.Font(
            12, wx.FONTFAMILY_DEFAULT, 0, weight=90, underline=False, faceName=""
        )

        # monitor_names_list contains all the signals that can be monitored
        self.monitor_names_list = []
        # monitor_list: [(device_id, output_id)]
        self.monitor_list = []
        self.monitor_selected_list = []
        # Uncomment when all modules ready
        # self.get_monitor_names()

        # Switch names and IDs
        # all switch ids. Set to empty initially
        self.switch_id_list = []
        # all switch names. Set to empty initially
        self.switch_name_list = [
            self.names.get_name_string(x) for x in self.switch_id_list
        ]
        self.switch_on_list = []
        self.switch_off_list = []
        # Uncomment when all modules ready
        # self.get_switch_names()

        # Temporarily set file to be not parsed
        self.is_parsed = False

        # configure initial parameters
        # Set default spin value
        self.spin_value = 10
        self.cycles_completed = 0

        # Canvas for drawing signals; Input the spin value here
        self.canvas = MyGLCanvas(self, devices, monitors, spin_value=self.spin_value)
        # Pass the monitor names list into monitored_signal_list attribute of canvas
        self.canvas.monitored_signal_list = self.monitor_names_list
        # Get window size
        self.window_size = self.GetClientSize()

        self.console_box = ConsoleBox(
            self, id=wx.ID_ANY, style=wx.TE_READONLY | wx.TE_MULTILINE | wx.TE_RICH2
        )
        self.console_box.SetFont(self.console_font)
        self.console_box.SetBackgroundColour("white")

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
            max=1000,
        )
        self.run_button = wx.Button(self, wx.ID_ANY, "Run")
        self.continue_button = wx.Button(self, wx.ID_ANY, "Continue")
        self.rerun_button = wx.Button(self, wx.ID_ANY, "Rerun")
        self.clear_console_button = wx.Button(self, wx.ID_ANY, "Clear Console")
        # Monitor and Switch Buttons
        self.monitor_button = wx.Button(self, wx.ID_ANY, "Choose Monitor")
        self.switch_button = wx.Button(self, wx.ID_ANY, "Choose Switch")

        # Set fonts for all
        self.run_button.SetFont(self.run_font)
        self.rerun_button.SetFont(self.run_font)
        self.continue_button.SetFont(self.run_font)
        self.clear_console_button.SetFont(self.run_font)
        self.monitor_button.SetFont(self.monitor_font)
        self.switch_button.SetFont(self.monitor_font)

        # Bind events to widgets
        # self.Bind(wx.EVT_MENU, self.on_menu)
        self.spin.Bind(wx.EVT_SPINCTRL, self.on_spin)
        self.run_button.Bind(wx.EVT_BUTTON, self.on_run_button)
        self.rerun_button.Bind(wx.EVT_BUTTON, self.on_rerun_button)
        self.clear_console_button.Bind(wx.EVT_BUTTON, self.on_clear_console_button)

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
        simulation_action_sizer = wx.BoxSizer(wx.VERTICAL)
        simulation_action_sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        simulation_action_sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
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
        simulation_action_sizer.Add(simulation_action_sizer_1, 1, wx.EXPAND, 0)
        simulation_action_sizer.Add(simulation_action_sizer_2, 1, wx.EXPAND, 0)
        simulation_action_sizer_1.Add(self.run_button, 1, wx.LEFT | wx.RIGHT, 3, 5)
        simulation_action_sizer_1.Add(self.continue_button, 1, wx.LEFT | wx.RIGHT, 3, 5)
        simulation_action_sizer_2.Add(self.rerun_button, 1, wx.LEFT | wx.RIGHT, 3, 5)
        simulation_action_sizer_2.Add(
            self.clear_console_button, 1, wx.LEFT | wx.RIGHT, 3, 5
        )
        simulation_sizer.Add(simulation_setting_sizer, 5, wx.ALL | wx.EXPAND, 5)
        simulation_sizer.Add(simulation_action_sizer, 5, wx.ALL | wx.EXPAND, 5)

        function_sizer.Add(self.monitor_button, 5, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
        function_sizer.Add(self.switch_button, 5, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

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
        # Update spin values in frame and canvas
        self.canvas.render(text)
        if spin_value > 100:
            dlg = wx.MessageDialog(
                self,
                "More than 100 cycles set to be run! Are you sure you want to continue?",
                "Warning",
                wx.OK | wx.ICON_WARNING,
            )
            dlg.ShowModal()
            if dlg == wx.OK:
                self.spin_value = spin_value
                self.canvas.spin_value = spin_value
            dlg.Destroy()

        else:
            self.spin_value = spin_value
            self.canvas.spin_value = spin_value

    def run_network(self, cycles):
        """Run the network for the specified number of simulation cycles.
        Return True if successfully run.
        """
        for i in range(cycles):
            if self.network.execute_network():
                self.monitors.record_signals()
            else:
                text = "Error! Network oscillating.\n"
                self.console_box.print_console_message(text)
                return False
        return True

    def on_run_button(self, event):
        """Handle the event when the user clicks the run button."""
        # text = "Run button pressed."
        # self.canvas.render(text)
        if self.is_parsed:
            # Reset the number of cycles for the canvas
            self.canvas.total_cycles = 0

            self.monitors.reset_monitors()
            self.devices.cold_startup()
            # If successfully run
            if self.run_network(self.spin_value):
                self.cycles_completed += self.spin_value
                text = "Now running for {no_cycles:.}!".format(no_cycles=str(self.spin_value))
                self.console_box.print_console_message(text)

                # Update canvas information
                # Add to the number of cycles run
                self.canvas.draw_signal()
                self.canvas.total_cycles += self.spin_value

        else:
            # Show error if file was not parsed correctly
            text = "Cannot run simulation. Please check your definition file.\n"
            self.console_box.print_console_message(text)

    def on_continue_button(self, event):
        """Continue a previously run simulation."""
        if self.is_parsed:
            if self.spin_value is not None:  # if the number of cycles provided is valid
                if self.cycles_completed == 0:
                    self.console_box.print_console_message(
                        "Error! No previous simulation. Please run first."
                    )
                # If the network is successfully run.
                elif self.run_network(cycles=self.spin_value):
                    self.cycles_completed += self.spin_value
                    text = "Now continuing for {no_cycles:.}!".format(
                        no_cycles=str(self.spin_value)
                    )
                    self.console_box.print_console_message(text)
                    # Update canvas information
                    # Add to the number of cycles run
                    self.canvas.draw_signal()
                    self.canvas.total_cycles += self.spin_value

        else:
            # Show error if file was not parsed correctly
            text = "Cannot continue running simulation. Please check your definition file.\n"
            self.console_box.print_console_message(text)

    def on_clear_console_button(self, event):
        self.console_box.clear_console()

    def on_rerun_button(self, event):
        """Run the simulation from scratch."""
        if self.is_parsed:
            self.cycles_completed = 0
            self.console_box.clear_console()
            self.on_run_button()
        else:
            text = "Cannot rerun simulation. Please check your definition file.\n"
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
                monitor_name = self.devices.get_signal_name(device.device_id, output_id)
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
                # Return indexes selected by the user
                selections = dlg.GetSelections()

                # Update monitor names selected by user
                self.update_monitors(selections)

            dlg.Destroy()
        else:
            # Show error if file was not parsed correctly
            text = "Cannot Show on Monitor. Please check your definition file.\n"
            self.console_box.print_console_message(text)

    def update_monitors(self, selections):
        """Update signals to be monitored and redraw on canvas"""
        self.monitor_selected_list = []
        for count in range(len(selections)):
            device_id, output_id = self.monitor_list[count]
            # If the index is selected by the user
            if count in self.monitor_selected_list:
                # Make monitor
                monitor_error = self.monitors.make_monitor(
                    device_id, output_id, self.cycles_completed
                )
                if monitor_error == self.monitors.NO_ERROR:
                    self.console_box.print_console_message("Successfully made monitor.")
                    # Append the name of the monitor into monitor_selected_list
                    self.monitor_selected_list.append(self.monitor_names_list[count])
                else:
                    self.console_box.print_console_message(
                        "Error! Could not make monitor."
                    )
        # Update the monitored_signal_list in the canvas element
        self.canvas.monitored_signal_list = self.monitor_selected_list
        self.canvas.draw_signal()

    def get_switch_names(self):
        """switch_id_list : list of the switch ids
        switch_names_list : list of switch names
        switch_on_list : list of switch names for switches set to High
        """
        # Get switch ids for all devices present
        self.switch_id_list = self.devices.find_devices(self.devices.SWITCH)
        self.switch_name_list = [
            self.names.get_name_string(x) for x in self.switch_id_list
        ]
        for i in range(len(self.switch_id_list)):
            count, switch_id = self.switch_id_list[i]
            if self.devices.get_device(switch_id).switch_state == self.devices.HIGH:
                # Add the name of the switch into the switch_on list
                self.switch_on_list.append(self.switch_name_list[count])

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
            dlg.Destroy()

        else:
            # Show error if file was not parsed correctly
            text = "Cannot Show on Monitor. Please check your definition file.\n"
            self.console_box.print_console_message(text)

    def update_switches(self, selections):
        """Update states of the switches and redraw on canvas"""
        self.switch_on_list = []
        self.switch_off_list = []

        for count in range(len(selections)):
            if count in self.switch_on_list:
                # Append the name of the switch into switch_on_list
                self.switch_on_list.append(self.switch_name_list[count])
            else:
                self.console_box.print_console_message("Error! Could not set switch.")
        # Unchosen switches in switch_off_list
        self.switch_off_list = [
            x for x in self.switch_name_list if x not in self.switch_on_list
        ]
        for switch in self.switch_on_list:
            switch_id = self.names.query(switch)
            # Set selected switches to be high
            self.devices.set_switch(switch_id, self.devices.HIGH)

        for switch in self.switch_off_list:
            switch_id = self.names.query(switch)
            # Set unselected switches to be low
            self.devices.set_switch(switch_id, self.devices.LOW)

        # Update devices in the canvas element
        self.canvas.devices = self.devices
