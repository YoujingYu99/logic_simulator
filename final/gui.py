"""Implement the graphical user interface for the Logic Simulator.

Used in the Logic Simulator project to enable the user to run the simulation
or adjust the network properties.

Classes:
--------
Gui - configures the main window and all the widgets.
"""
import wx
import logging

from gl_canvas import MyGLCanvas
from frame_elements import FileMenu, HelpMenu, AboutMenu, \
    ConsoleBox, CycleNumberText

_ = wx.GetTranslation


class Gui(wx.Frame):
    """Configure the main window and all the widgets.

    This class provides a graphical user interface for the Logic Simulator
    and enables the user to change the circuit properties and run
    simulations.

    Parameters
    ----------
    title: title of the window.
    Public methods
    --------------
    configure_style(self): Configure CSS stylesheet.

    on_spin(self, event): Event handler for when the user changes the spin
                           control value.

    check_cycle(self): Check whether the number of cycles is sensible
                            to be run.

    run_network(self, cycles): Check whether the cycle is successfully run.

    on_run_button(self, spin_value): Event handler for when the user clicks
                            the run button.

    on_clear_console_button(self): Event handler for when the user clicks
                            the clear console button.

    on_rerun_button(self, spin_value): Event handler for when the user
                            clicks the rerun button.

    on_continue_button(self, spin_value): Event handler for when the user
                            clicks the continue button.

    get_monitor_names(self): Return monitor_list and monitor_names_list.

    on_monitor_button(self): Event handler for when the user chooses a few
                            monitors and draw the signals.

    update_monitor(self): Event handler for when the monitor states are
                            updated.

    get_switch_names(self): Return switch_name_list and switch_on_list.

    on_switch_button(self): Event handler for when the user chooses a few
                            switches.
    update_switches(self): Event handler for when the switch state changes.

    get_inputs_output(self): Get all inputs and output names in network.

    on_make_connection_button(self):Event handler for when the user makes
                            connections.

    on_remove_connection_button(self):Event handler for when the user removes
                            connections.

    clear_previous_file(self): Event handler for when the user opens another
                            definition file.
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
        # Use CSS stylesheet
        self.style = wx.GetApp().stylesheet
        self.configure_style()

        # Set parameters
        self.cycle_text_colour = (0, 0, 0)
        # Set fonts
        self.cycle_font = wx.Font(
            11,
            wx.FONTFAMILY_SWISS,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_NORMAL,
            underline=False,
        )
        self.monitor_font = wx.Font(
            14,
            wx.FONTFAMILY_SWISS,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_NORMAL,
            underline=False,
        )
        self.run_font = wx.Font(
            12,
            wx.FONTFAMILY_SWISS,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_NORMAL,
            underline=False,
        )
        self.console_font = wx.Font(
            12,
            wx.FONTFAMILY_TELETYPE,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_NORMAL,
            underline=False,
        )

        # Monitor_names_list contains all the signals that can be monitored
        self.monitor_names_list = []
        # monitor_id_list: [(device_id, output_id)]
        self.monitor_id_list = []
        self.monitored_list = []
        self.unmonitored_list = []

        # Switch names and IDs
        # All switch ids. Set to empty initially
        self.switch_id_list = []
        # All switch names. Set to empty initially
        self.switch_name_list = []
        self.switch_on_list = []
        self.switch_off_list = []
        # All inputs and outputs in the network
        self.input_list = []
        self.output_list = []

        # Temporarily set file to be not parsed
        self.is_parsed = False
        self.cycle_ok = False

        # Configure initial parameters
        # Set default spin value
        self.spin_value = 10
        self.cycles_completed = 0

        # Canvas for drawing signals; Input the spin value here
        self.canvas = MyGLCanvas(
            self, devices, monitors, cycles_completed=self.cycles_completed
        )
        # Pass the monitor names list into canvas
        self.canvas.monitored_signal_list = self.monitored_list
        # Get window size
        self.window_size = self.GetClientSize()

        self.console_box = ConsoleBox(
            self, id=wx.ID_ANY, style=wx.TE_READONLY | wx.TE_MULTILINE
            | wx.TE_RICH2
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
        menuBar.Append(fileMenu, "".join(("&", _("File"))))
        menuBar.Append(helpMenu, "".join(("&", _("Help"))))
        menuBar.Append(aboutMenu, "".join(("&", _("About"))))

        # Set menubar
        self.SetMenuBar(menuBar)

        # Configure console properties
        self.console_text = _("Welcome to Logic Simulation App!")

        # Configure the widgets
        self.text = CycleNumberText(self, wx.ID_ANY, _("Number of Cycles"))
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
        self.run_button = wx.Button(self, wx.ID_ANY, _("Run"))
        self.continue_button = wx.Button(self, wx.ID_ANY, _("Continue"))
        self.rerun_button = wx.Button(self, wx.ID_ANY, _("Rerun"))
        self.clear_console_button = \
            wx.Button(self, wx.ID_ANY, _("Clear Console"))
        # Monitor and Switch Buttons
        self.monitor_button = wx.Button(self, wx.ID_ANY, _("Choose Monitor"))
        self.switch_button = wx.Button(self, wx.ID_ANY, _("Choose Switch"))
        self.make_connection_button = wx.Button(self, wx.ID_ANY,
                                                _("Make Connection"))
        self.remove_connection_button = wx.Button(self, wx.ID_ANY,
                                                  _("Remove Connection"))

        # Set fonts for all
        self.run_button.SetFont(self.run_font)
        self.rerun_button.SetFont(self.run_font)
        self.continue_button.SetFont(self.run_font)
        self.clear_console_button.SetFont(self.run_font)
        self.monitor_button.SetFont(self.monitor_font)
        self.switch_button.SetFont(self.monitor_font)
        self.make_connection_button.SetFont(self.run_font)
        self.remove_connection_button.SetFont(self.run_font)

        # Bind events to widgets
        self.spin.Bind(wx.EVT_SPINCTRL, self.on_spin)
        self.run_button.Bind(wx.EVT_BUTTON, self.on_run_button)
        self.rerun_button.Bind(wx.EVT_BUTTON, self.on_rerun_button)
        self.clear_console_button.Bind(wx.EVT_BUTTON,
                                       self.on_clear_console_button)
        self.continue_button.Bind(wx.EVT_BUTTON, self.on_continue_button)
        self.monitor_button.Bind(wx.EVT_BUTTON, self.on_monitor_button)
        self.switch_button.Bind(wx.EVT_BUTTON, self.on_switch_button)
        # Make and remove connections
        self.make_connection_button.Bind(wx.EVT_BUTTON,
                                         self.on_make_connection_button)
        self.remove_connection_button.Bind(wx.EVT_BUTTON,
                                           self.on_remove_connection_button)

        # Configure sizers for layout
        # Controls the entire screen
        top_level_sizer = wx.BoxSizer(wx.VERTICAL)
        # Contains canvas and sidebar
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # Contains simulation/function sizers
        side_sizer = wx.BoxSizer(wx.VERTICAL)
        # Contains the console
        console_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Sidebar sizers
        simulation_sizer = wx.StaticBoxSizer(wx.VERTICAL, self)
        simulation_setting_sizer = wx.BoxSizer(wx.HORIZONTAL)
        simulation_action_sizer = wx.BoxSizer(wx.VERTICAL)
        simulation_action_sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        simulation_action_sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        function_sizer = wx.StaticBoxSizer(wx.VERTICAL, self)
        connection_sizer = wx.BoxSizer(wx.HORIZONTAL)

        top_level_sizer.Add(main_sizer, 5, wx.ALL | wx.EXPAND, 5)
        top_level_sizer.Add(console_sizer, 2, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(self.canvas, 5, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(side_sizer, 1, wx.EXPAND | wx.ALL, 5)
        side_sizer.Add(simulation_sizer, 1, wx.EXPAND, 0)
        side_sizer.Add(function_sizer, 1, wx.EXPAND, 0)

        # Side sizer configuration
        simulation_setting_sizer.Add(self.text, 1, wx.ALL, 10)
        simulation_setting_sizer.Add(self.spin, 1, wx.ALL, 10)
        simulation_action_sizer.Add(simulation_action_sizer_1,
                                    1, wx.EXPAND, 0)
        simulation_action_sizer.Add(simulation_action_sizer_2,
                                    1, wx.EXPAND, 0)
        simulation_action_sizer_1.Add(self.run_button, 1,
                                      wx.LEFT | wx.RIGHT, 3, 5)
        simulation_action_sizer_1.Add(self.continue_button, 1,
                                      wx.LEFT | wx.RIGHT, 3, 5)
        simulation_action_sizer_2.Add(self.rerun_button, 1,
                                      wx.LEFT | wx.RIGHT, 3, 5)
        simulation_action_sizer_2.Add(
            self.clear_console_button, 1, wx.LEFT | wx.RIGHT, 3, 5
        )
        simulation_sizer.Add(simulation_setting_sizer, 5,
                             wx.ALL | wx.EXPAND, 5)
        simulation_sizer.Add(simulation_action_sizer, 5,
                             wx.ALL | wx.EXPAND, 5)

        function_sizer.Add(self.monitor_button, 5,
                           wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
        function_sizer.Add(self.switch_button, 5,
                           wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
        function_sizer.Add(connection_sizer, 5,
                           wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
        connection_sizer.Add(self.make_connection_button, 1,
                             wx.LEFT | wx.RIGHT, 3, 5)
        connection_sizer.Add(self.remove_connection_button, 1,
                             wx.LEFT | wx.RIGHT, 3, 5)

        # Console sizer configuration
        console_sizer.Add(self.console_box, 5, wx.EXPAND | wx.ALL, 5)
        console_sizer.SetMinSize(self.window_size[0],
                                 self.window_size[1] / 3)

        self.SetSizeHints(600, 600)
        self.SetSizer(top_level_sizer)

        # Configure the loggers
        self.scanner_logger = logging.getLogger("scanner")
        self.parser_logger = logging.getLogger("parser")
        logging.basicConfig(level=logging.DEBUG)

    def configure_style(self):
        """Configure the CSS stylesheet in the element."""
        self.style.apply_rules(self)

    def on_spin(self, event):
        """Handle the event when the user changes the spin control value."""
        spin_value = self.spin.GetValue()
        text = "".join([_("New spin control value: "), str(spin_value)])
        # Update spin values in frame and canvas
        self.canvas.render(text)
        self.spin_value = spin_value

    def check_cycle(self):
        """Check whether the number of cycles set to run is sensible."""
        # Warning if too many cycles set
        if self.spin_value >= 1000:
            dlg = wx.MessageDialog(
                self,
                _("More than 1000 cycles set to be run. "
                  "Please change to a lower value of runs."),
                _("Warning"),
                wx.OK | wx.ICON_WARNING,
            )
            dlg.ShowModal()
            dlg.Destroy()
            self.cycle_ok = False
        # Warning if running more than 100 cycles
        elif 100 < self.spin_value < 1000:
            dlg = wx.MessageDialog(
                self,
                _("More than 100 cycles set to be run! Are you sure you"
                  " want to continue?"),
                _("Warning"),
                wx.YES_NO | wx.ICON_QUESTION,
            )
            dlg.ShowModal()
            if dlg.ShowModal() == wx.ID_YES:
                self.cycle_ok = True
            dlg.Destroy()
        else:
            self.cycle_ok = True

    def run_network(self, cycles):
        """Run the network for the specified number of simulation cycles.

        Return True if successfully run.
        """
        for i in range(cycles):
            if self.network.execute_network():
                self.monitors.record_signals()
            else:
                text = "".join((_("Error! Network oscillating."), "\n"))
                self.console_box.print_console_message(text)
                return False
        return True

    def on_run_button(self, event):
        """Handle the event when the user clicks the run button."""
        # Check whether a sensible number of cycles is run
        self.check_cycle()
        if self.cycle_ok:
            if self.is_parsed:
                # Reset the number of cycles
                self.cycles_completed = 0
                self.monitors.reset_monitors()
                self.devices.cold_startup()
                # If successfully run
                if self.run_network(self.spin_value):
                    self.cycles_completed += self.spin_value
                    self.canvas.monitored_signal_list = self.monitored_list
                    # Update cycles run
                    self.canvas.cycles_completed = self.cycles_completed
                    text = "".join([_("Running for "),
                                    str(self.spin_value), _(" cycles."), "\n"])
                    self.console_box.print_console_message(text)
            else:
                # Show error if file was not parsed correctly
                text = "".join((_("Cannot run simulation. Please check your "
                                  "definition file."), "\n"))
                self.console_box.print_console_message(text)

    def on_continue_button(self, event):
        """Continue a previously run simulation."""
        # Check whether a sensible number of cycles is run
        self.check_cycle()
        if self.cycle_ok:
            if self.is_parsed:
                if self.spin_value is not None:
                    # If no previous cycles have run
                    if self.cycles_completed == 0:
                        self.console_box.print_console_message(
                            _("Error! No previous simulation. "),
                            "".join((_("Please run first."), "\n"))
                        )
                    # If the network is successfully run.
                    elif self.run_network(cycles=self.spin_value):
                        self.cycles_completed += self.spin_value
                        # Update canvas cycles
                        self.canvas.cycles_completed = self.cycles_completed
                        text = "".join(
                            [
                                _("Continuing for "),
                                str(self.spin_value),
                                _(" cycles,"),
                                _(" a total of "),
                                str(self.cycles_completed),
                                _(" cycles run."), "\n",
                            ]
                        )
                        self.console_box.print_console_message(text)
                        # Update canvas information
                        # Add to the number of cycles run

            else:
                # Show error if file was not parsed correctly
                text = "".join((
                    _("Cannot continue running simulation. Please check"),
                    _("your definition file."), "\n"
                ))
                self.console_box.print_console_message(text)

    def on_clear_console_button(self, event):
        """Clear the entire console output."""
        self.console_box.clear_console()

    def on_rerun_button(self, event):
        """Run the simulation from scratch."""
        # Check whether a sensible number of cycles is run
        self.check_cycle()
        if self.cycle_ok:
            if self.is_parsed:
                # Reset cycles completed number
                self.cycles_completed = 0
                self.canvas.cycles_completed = self.cycles_completed
                # Reset console to be clear
                self.console_box.clear_console()
                self.on_run_button(None)
            else:
                text = "".join((
                    _("Cannot rerun simulation. Please check "),
                    _("your definition file."), "\n"
                ))
                self.console_box.print_console_message(text)

    def get_monitor_names(self):
        """Get all monitor names, id and monitored and unmonitored list.

        monitored_list/unmonitored_list : names of signals
                                    monitored/unmonitored.
        monitor_names_list :all monitor names.
        """
        # Set monitored and unmonitored lists
        self.monitored_list = self.monitors.get_signal_names()[0]
        self.unmonitored_list = self.monitors.get_signal_names()[1]
        # Append list to get a full list of monitor names
        self.monitor_names_list = self.monitored_list \
            + self.unmonitored_list

        # To get monitor ids
        for monitor_name in self.monitor_names_list:
            device_id, output_id = self.devices.get_signal_ids(monitor_name)
            # Append device id, output id to the monitor id list
            self.monitor_id_list.append((device_id, output_id))

    def on_monitor_button(self, event):
        """Choose signals to monitor and draw."""
        if self.is_parsed:
            # Renew the names for monitors
            self.get_monitor_names()
            dlg = wx.MultiChoiceDialog(
                self,
                _("Choose the Signals You Wish to Monitor"),
                _("Monitored Signals"),
                self.monitor_names_list,
            )
            monitor_on_ids = [self.monitor_names_list.index(j)
                              for j in self.monitored_list]
            # Preselet
            dlg.SetSelections(monitor_on_ids)

            if dlg.ShowModal() == wx.ID_OK:
                # Return indexes selected by the user
                selections = dlg.GetSelections()
                # Update monitor names selected by user
                self.update_monitors(selections)

            dlg.Destroy()
        else:
            # Show error if file was not parsed correctly
            text = "".join((_("Cannot Show on Monitor. Please check your "
                              "definition file."), "\n"))
            self.console_box.print_console_message(text)

    def update_monitors(self, selections):
        """Update signals to be monitored and redraw on canvas."""
        # Make monitored list based on user selections
        new_monitored_list = [self.monitor_names_list[i]
                              for i in selections]

        for monitored_signal in new_monitored_list:
            # Get device and output ids
            device_id, output_id = \
                self.devices.get_signal_ids(monitored_signal)
            # If not already monitored
            if monitored_signal not in self.monitored_list:
                # Make monitor
                monitor_error = self.monitors.make_monitor(
                    device_id, output_id, self.cycles_completed
                )
                if monitor_error == self.monitors.NO_ERROR:
                    self.console_box.print_console_message(
                        "".join((_("Successfully made monitor."),
                                 "\n"))
                    )
                else:
                    self.console_box.print_console_message(
                        "".join((_("Error! Could not make monitor."),
                                 "\n"))
                    )
        # Update the monitored list
        self.monitored_list = new_monitored_list
        # Update the monitored_signal_list in the canvas element
        self.canvas.monitored_signal_list = self.monitored_list

    def get_switch_names(self):
        """Get all switch names, ids and switches on.

        switch_names_list : list of switch names.
        switch_id_list : list of the switch ids.
        switch_on_list : list of switch names for switches set to High.
        """
        # Get switch ids for all devices present
        self.switch_id_list = self.devices.find_devices(self.devices.SWITCH)
        self.switch_name_list = [
            self.names.get_name_string(x) for x in self.switch_id_list
        ]
        for i in range(len(self.switch_id_list)):
            switch_id = self.switch_id_list[i]
            switch_name = self.switch_name_list[i]
            # If the state of the switch is HIGH
            if self.devices.get_device(switch_id).switch_state \
                    == self.devices.HIGH:
                # Add the name of the switch into the switch_on list
                self.switch_on_list.append(switch_name)

    def on_switch_button(self, event):
        """Set switch to desired state."""
        if self.is_parsed:
            dlg = wx.MultiChoiceDialog(
                self,
                _("Choose the switches to be set to 1"),
                _("Switch Settings"),
                self.switch_name_list,
            )
            switch_on_ids = [self.switch_name_list.index(j)
                             for j in self.switch_on_list]
            dlg.SetSelections(switch_on_ids)

            if dlg.ShowModal() == wx.ID_OK:
                selections = dlg.GetSelections()
                # Update switches
                self.update_switches(selections)
            dlg.Destroy()

        else:
            # Show error if file was not parsed correctly
            text = "".join((_("Cannot Show on Monitor. Please check your "
                              "definition file."), "\n"))
            self.console_box.print_console_message(text)

    def update_switches(self, selections):
        """Update states of the switches in devices and pass into canvas."""
        # Reset the list of switches on depending on user selection
        self.switch_on_list = [self.switch_name_list[i] for i in selections]
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
        self.console_box.print_console_message(
            "".join((_("Successfully set the state of switches."),
                     "\n")))

    def get_inputs_outputs(self):
        """Get all inputs and outputs in network."""
        input_list = []
        output_list = []
        for device in self.devices.devices_list:
            device_name = self.names.get_name_string(
                device.device_id)
            for key in device.inputs.keys():
                full_input_name = device_name + "." \
                    + self.names.get_name_string(key)
                input_list.append(full_input_name)
                # Check outputs
            for key in device.outputs.keys():
                try:
                    output_name = self.names.get_name_string(
                        key)
                    full_output_name = device_name + "." + output_name
                except BaseException:
                    full_output_name = device_name
                output_list.append(full_output_name)

        self.input_list = input_list
        self.output_list = output_list

    def on_make_connection_button(self, event):
        """Make connection between two inputs/outputs."""
        chosen_input = None
        chosen_output = None
        if self.is_parsed:
            # Dialog for choosing input
            input_dlg = wx.SingleChoiceDialog(
                self,
                _("Choose the Input You Wish to Connect"),
                _("Input of Connection"),
                self.input_list,
            )

            if input_dlg.ShowModal() == wx.ID_OK:
                # Return indexes selected by the user
                selected_input = input_dlg.GetStringSelection()
                chosen_input = selected_input
            input_dlg.Destroy()

            output_dlg = wx.SingleChoiceDialog(
                self,
                _("Choose the Output You Wish to Connect"),
                _("Output of Connection"),
                self.output_list,
            )

            if output_dlg.ShowModal() == wx.ID_OK:
                # Return indexes selected by the user
                selected_output = output_dlg.GetStringSelection()
                chosen_output = selected_output
            output_dlg.Destroy()

            # If both chosen
            if chosen_input and chosen_output:
                first_device_id, first_port_id = \
                    self.devices.get_signal_ids(chosen_input)
                second_device_id, second_port_id = \
                    self.devices.get_signal_ids(
                        chosen_output)
                # Get output and port ids
                print(_('input name'), chosen_input)
                print(_('output name'), chosen_output)
                print(_('first device, port'), first_device_id, first_port_id)
                print(_('second device, port'), second_device_id,
                      second_port_id)
                connection_error = self.network.make_connection(
                    first_device_id, first_port_id,
                    second_device_id, second_port_id
                )

                if connection_error == self.network.NO_ERROR:
                    self.console_box.print_console_message(
                        "".join((_("Successfully made connection."),
                                 "\n"))
                    )
                else:
                    self.console_box.print_console_message(
                        "".join((_("Error! Could not make connection."),
                                 "\n"))
                    )

    def on_remove_connection_button(self, event):
        """Remove connection between two inputs/outputs."""
        chosen_input = None
        chosen_output = None
        if self.is_parsed:
            # Dialog for choosing input
            self.get_inputs_outputs()
            input_dlg = wx.SingleChoiceDialog(
                self,
                _("Choose the Input of the Connection You Wish to Remove"),
                _("Input of Connection"),
                self.input_list,
            )

            if input_dlg.ShowModal() == wx.ID_OK:
                # Return indexes selected by the user
                selected_input = input_dlg.GetStringSelection()
                chosen_input = selected_input
            input_dlg.Destroy()

            output_dlg = wx.SingleChoiceDialog(
                self,
                _("Choose the Output of the Connection You Wish to Remove"),
                _("Output of Connection"),
                self.output_list,
            )

            if output_dlg.ShowModal() == wx.ID_OK:
                # Return indexes selected by the user
                selected_output = output_dlg.GetStringSelection()
                chosen_output = selected_output
            output_dlg.Destroy()
            # If both chosen
            if chosen_input and chosen_output:
                # Get output and port ids
                first_device_id, first_port_id = \
                    self.devices.get_signal_ids(chosen_input)
                second_device_id, second_port_id = \
                    self.devices.get_signal_ids(chosen_output)
                connection_error = self.network.remove_connection(
                    first_device_id, first_port_id,
                    second_device_id, second_port_id
                )
                if connection_error == self.network.NO_ERROR:
                    self.console_box.print_console_message(
                        "".join((_("Successfully removed connection."),
                                 "\n"))
                    )
                else:
                    self.console_box.print_console_message(
                        "".join((_("Error! Could not remove connection."),
                                 "\n"))
                    )

    def clear_previous_file(self):
        """Reinitialise everything when new definition file chosen."""
        # Set all input parameters to None/empty
        self.network = None
        self.names = None
        self.devices = None
        self.monitors = None
        self.monitor_names_list = []
        self.monitor_id_list = []
        self.monitored_list = []
        self.unmonitored_list = []

        # Switch names and IDs set empty
        self.switch_id_list = []
        self.switch_name_list = []
        self.switch_on_list = []
        self.switch_off_list = []
        self.input_list = []
        self.output_list = []

        # Set file to be not parsed
        self.is_parsed = False

        # Set default spin value
        self.spin_value = 10
        self.cycles_completed = 0

        # Configure console properties
        self.console_text = _("Welcome to Logic Simulation App!")

        # Configure the loggers
        self.scanner_logger = logging.getLogger("scanner")
        self.parser_logger = logging.getLogger("parser")
        logging.basicConfig(level=logging.DEBUG)

        # Reinitialise the canvas elements
        self.canvas.devices = None
        self.canvas.monitors = None
        self.canvas.monitored_signal_list = []
        self.canvas.cycles_completed = 0
