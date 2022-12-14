"""Draw the canvas and subsequent elements for the Graphical User Interface.

Classes:
--------
MyGLCanvas - handles all canvas drawing operations.
"""

import wx
import wx.glcanvas as wxcanvas
from OpenGL import GL, GLUT
_ = wx.GetTranslation


class MyGLCanvas(wxcanvas.GLCanvas):
    """Handle all drawing operations.

    This class contains functions for drawing onto the canvas. It
    also contains handlers for events relating to the canvas.

    Parameters
    ----------
    parent: parent window.
    devices: instance of the devices.Devices() class.
    monitors: instance of the monitors.Monitors() class.

    Public methods
    --------------
    init_gl(self): Configures the OpenGL context.
    render(self, text): Handles all drawing operations.
    on_paint(self, event): Handles the paint event.
    on_size(self, event): Handles the canvas resize event.
    on_mouse(self, event): Handles mouse events.
    render_text(self, text, x_pos, y_pos): Handles text drawing
                                           operations.
    draw_grid(self, spin_value): Draw grid axes on the displayed signals.
    draw_signal(self): Draw signals chosen.
    """

    def __init__(self, parent, devices, monitors, cycles_completed):
        """Initialise canvas properties and useful variables."""
        super().__init__(
            parent,
            -1,
            attribList=[
                wxcanvas.WX_GL_RGBA,
                wxcanvas.WX_GL_DOUBLEBUFFER,
                wxcanvas.WX_GL_DEPTH_SIZE,
                16,
                0,
            ],
        )
        GLUT.glutInit()
        self.init = False
        self.context = wxcanvas.GLContext(self)

        # Initialise variables for panning
        self.pan_x = 0
        self.pan_y = 0
        self.last_mouse_x = 0  # previous mouse x position
        self.last_mouse_y = 0  # previous mouse y position

        # Initialise variables for zooming
        self.zoom = 1

        # Initialise variables for diagram dimensions
        self.min_width = 0
        self.min_width = 0
        self.min_height = 0

        # Initialise variables for drawing signals
        # Grid starting point
        self.grid_origin = 0
        # width, height
        canvas_width, canvas_height = self.GetClientSize()
        self.canvas_origin = [
            (canvas_width - self.min_width) / 2,
            (canvas_height - self.min_height) / 2,
        ]
        # Signal parameters
        # Blue, red, black colours for signals
        self.signal_colours = [(0.0, 0.0, 1.0), (1.0, 0.0, 0.0),
                               (0.0, 0.0, 0.0)]
        self.signal_height = 50
        self.signal_cycle_width = 40
        self.signal_y_distance = 20
        # Axis parameters
        self.num_period_display = 10
        self.y_axis_offset = 50
        self.x_axis_offset = 50
        self.x_grid_offset = 5
        self.y_grid_offset_lower = 20
        self.y_grid_offset_upper = 10
        self.tick_width = 3
        self.small_font = GLUT.GLUT_BITMAP_HELVETICA_12
        self.label_font = GLUT.GLUT_BITMAP_9_BY_15
        self.label_size = 20
        self.label_width = 0

        # Set monitors to be drawn
        self.devices = devices
        self.monitors = monitors
        # Initialise the monitored signals list
        self.monitored_signal_list = []
        # Cycles already run in total
        self.cycles_completed = cycles_completed

        # Bind events to the canvas
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.on_mouse)

    def init_gl(self):
        """Configure and initialise the OpenGL context."""
        size = self.GetClientSize()
        self.SetCurrent(self.context)
        GL.glDrawBuffer(GL.GL_BACK)
        # Set white background colour
        GL.glClearColor(1.0, 1.0, 1.0, 1.0)
        GL.glViewport(0, 0, size.width, size.height)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GL.glOrtho(0, size.width, 0, size.height, -1, 1)
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()
        GL.glTranslated(self.pan_x, self.pan_y, 0.0)
        GL.glScaled(self.zoom, self.zoom, self.zoom)

    def render(self, text):
        """Handle all drawing operations."""
        self.SetCurrent(self.context)
        if not self.init:
            # Configure the viewport, modelview and projection matrices
            self.init_gl()
            self.init = True

        # Clear everything
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        # Draw specified text at position (10, 10)
        self.render_text(text, 10, 10)
        if self.monitored_signal_list:
            self.draw_signal()
        else:
            pass
        # We have been drawing to the back buffer, flush the
        # graphics pipeline
        # and swap the back buffer to the front
        GL.glFlush()
        self.SwapBuffers()

    def on_paint(self, event):
        """Handle the paint event."""
        self.SetCurrent(self.context)
        if not self.init:
            # Configure the viewport, modelview and projection matrices
            self.init_gl()
            self.init = True

        size = self.GetClientSize()
        text = "".join(
            [
                _("Canvas redrawn on paint event, size is "),
                str(size.width),
                ", ",
                str(size.height),
            ]
        )
        self.render(text)

    def on_size(self, event):
        """Handle the canvas resize event."""
        # Forces reconfiguration of the viewport, modelview and projection
        # matrices on the next paint event
        self.init = False

    def on_mouse(self, event):
        """Handle mouse events."""
        text = ""
        # Calculate object coordinates of the mouse position
        size = self.GetClientSize()
        ox = (event.GetX() - self.pan_x) / self.zoom
        oy = (size.height - event.GetY() - self.pan_y) / self.zoom
        old_zoom = self.zoom
        if event.ButtonDown():
            self.last_mouse_x = event.GetX()
            self.last_mouse_y = event.GetY()
            text = "".join(
                [
                    _("Mouse button pressed at: "),
                    str(event.GetX()),
                    ", ",
                    str(event.GetY()),
                ]
            )
        if event.ButtonUp():
            text = "".join(
                [
                    _("Mouse button released at: "),
                    str(event.GetX()),
                    ", ",
                    str(event.GetY()),
                ]
            )
        if event.Leaving():
            text = "".join(
                [_("Mouse left canvas at: "), str(event.GetX()), ", ",
                 str(event.GetY())]
            )
        if event.Dragging():
            self.pan_x += event.GetX() - self.last_mouse_x
            self.pan_y -= event.GetY() - self.last_mouse_y
            self.last_mouse_x = event.GetX()
            self.last_mouse_y = event.GetY()
            self.init = False
            text = "".join(
                [
                    _("Mouse dragged to: "),
                    str(event.GetX()),
                    ", ",
                    str(event.GetY()),
                    _(". Pan is now: "),
                    str(self.pan_x),
                    ", ",
                    str(self.pan_y),
                ]
            )
        if event.GetWheelRotation() < 0:
            self.zoom *= 1.0 + (event.GetWheelRotation() /
                                (20 * event.GetWheelDelta()))
            # Adjust pan so as to zoom around the mouse position
            self.pan_x -= (self.zoom - old_zoom) * ox
            self.pan_y -= (self.zoom - old_zoom) * oy
            self.init = False
            text = "".join(
                [_("Negative mouse wheel rotation. Zoom is now: "),
                 str(self.zoom)]
            )
        if event.GetWheelRotation() > 0:
            self.zoom /= 1.0 - (event.GetWheelRotation() /
                                (20 * event.GetWheelDelta()))
            # Adjust pan so as to zoom around the mouse position
            self.pan_x -= (self.zoom - old_zoom) * ox
            self.pan_y -= (self.zoom - old_zoom) * oy
            self.init = False
            text = "".join(
                [_("Positive mouse wheel rotation. Zoom is now: "),
                 str(self.zoom)]
            )
        if text:
            self.render(text)
        else:
            self.Refresh()  # triggers the paint event

    def render_text(self, text, x_pos, y_pos):
        """Handle text drawing operations."""
        GL.glColor3f(0, 0, 0)
        GL.glRasterPos2f(x_pos, y_pos)
        font = GLUT.GLUT_BITMAP_HELVETICA_12

        for character in text:
            if character == "\n":
                y_pos = y_pos - 20
                GL.glRasterPos2f(x_pos, y_pos)
            else:
                GLUT.glutBitmapCharacter(font, ord(character))

    def draw_grid(self, spin_value):
        """Draw grid axes on the displayed signals."""
        # Period of cycles
        cycle_period = spin_value // (self.num_period_display - 1)

        # Draw x axis. Set x starting points
        x_left = self.canvas_origin[0]
        if spin_value <= 10:
            x_right = (
                self.canvas_origin[0]
                + spin_value * self.signal_cycle_width
                + x_left
                + self.x_axis_offset
                + self.y_axis_offset
            )
        else:
            x_right = (
                self.canvas_origin[0]
                + (self.num_period_display + 5) * self.signal_cycle_width
                + x_left
                + self.x_axis_offset
                + self.y_axis_offset
            )

        y_bottom = self.canvas_origin[1]

        # Draw x axis
        GL.glColor3f(0, 0, 0)
        GL.glBegin(GL.GL_LINE_STRIP)
        GL.glVertex2f(x_left, y_bottom + self.x_axis_offset)
        GL.glVertex2f(x_right, y_bottom + self.x_axis_offset)
        GL.glEnd()

        # Draw x grid ticks
        x_grid_start = self.canvas_origin[0] + self.x_axis_offset \
            + self.y_axis_offset
        if spin_value <= 10:
            # Interval for the vertical grid lines
            x_grid_interval = self.signal_cycle_width
            # Positions of x ticks
            # Add one more tick at the end
            x_tick_x_list = [
                (index * x_grid_interval) + x_grid_start
                for index in range(spin_value + 1)
            ]
        else:
            if 10 <= spin_value < 20:
                x_grid_interval = self.signal_cycle_width / 2
            else:
                x_grid_interval = self.signal_cycle_width / cycle_period
            # Only show 8 ticks if spin value greater than 10
            num_list = list(range(self.num_period_display))
            tick_list = [(cycle_period + 1) * tick for tick in num_list]
            x_tick_x_list = [(i * x_grid_interval) + x_grid_start
                             for i in tick_list]
        x_tick_y_low = y_bottom + self.x_axis_offset - self.tick_width / 2
        x_tick_y_high = y_bottom + self.x_axis_offset + self.tick_width / 2
        for i in range(len(x_tick_x_list)):
            GL.glColor3f(0, 0, 0)
            GL.glBegin(GL.GL_LINE_STRIP)
            GL.glVertex2f(x_tick_x_list[i], x_tick_y_low)
            GL.glVertex2f(x_tick_x_list[i], x_tick_y_high)
            GL.glEnd()

            # Label x axis(cycle number)
            GL.glColor3f(0, 0, 0)
            x_pos = x_tick_x_list[i]
            y_pos = y_bottom + self.x_axis_offset / 2
            GL.glRasterPos2f(x_pos, y_pos)
            font = self.small_font
            if spin_value <= 10:
                label = str(i)
            else:
                label = str(tick_list[i])
            for character in label:
                GLUT.glutBitmapCharacter(font, ord(character))

        # Label x axis
        text = _("No. of Cycles")
        font = self.label_font
        x_pos_x_label = x_right + self.y_axis_offset / 2
        y_pos_x_label = y_bottom + self.x_axis_offset
        GL.glColor3f(0, 0, 0)
        GL.glRasterPos2f(x_pos_x_label, y_pos_x_label)
        for character in text:
            GLUT.glutBitmapCharacter(font, ord(character))

        # Draw y axis. Set y starting points
        x_left = self.canvas_origin[0] + self.y_axis_offset
        y_height_needed = (
            len(self.monitored_signal_list)
            * (self.y_grid_offset_lower + self.signal_height
               + self.signal_y_distance)
            + self.y_grid_offset_upper
            + self.x_axis_offset
        )
        y_top = y_bottom + y_height_needed

        # Draw y axis
        GL.glColor3f(0, 0, 0)
        GL.glBegin(GL.GL_LINE_STRIP)
        GL.glVertex2f(x_left, y_bottom + self.x_axis_offset / 2)
        GL.glVertex2f(x_left, y_top)
        GL.glEnd()

        # Draw y_grid for signal cycles
        for i in range(len(x_tick_x_list)):
            # Grey gridlines
            GL.glColor3f(0.7, 0.8, 0.8)
            GL.glBegin(GL.GL_LINE_STRIP)
            GL.glVertex2f(x_tick_x_list[i], x_tick_y_low)
            GL.glVertex2f(x_tick_x_list[i], y_top)
            GL.glEnd()

        # Draw y grid for many signals
        num_signals = len(self.monitored_signal_list)
        y_tick_left = x_left - self.tick_width / 2
        y_tick_right = x_left + self.tick_width / 2
        for count in range(num_signals):
            # Draw y grid ticks
            # Grid at 0
            zero_pos = (
                y_bottom
                + self.x_axis_offset
                + self.y_grid_offset_lower
                + count * (self.signal_y_distance + self.signal_height)
            )
            # Grid at 0
            GL.glColor3f(0, 0, 0)
            GL.glBegin(GL.GL_LINE_STRIP)
            GL.glVertex2f(y_tick_left, zero_pos)
            GL.glVertex2f(y_tick_right, zero_pos)
            GL.glEnd()

            # Light grey grid lines
            GL.glColor3f(0.88, 0.92, 0.92)
            GL.glBegin(GL.GL_LINE_STRIP)
            GL.glVertex2f(y_tick_left, zero_pos)
            GL.glVertex2f(x_right, zero_pos)
            GL.glEnd()

            # Label 0
            GL.glColor3f(0, 0, 0)
            x_pos_0 = x_left - self.label_size
            y_pos_0 = zero_pos
            GL.glRasterPos2f(x_pos_0, y_pos_0)
            font = self.small_font
            label_zero = "0"
            GLUT.glutBitmapCharacter(font, ord(label_zero))

            # Grid at 1
            GL.glColor3f(0, 0, 0)
            GL.glBegin(GL.GL_LINE_STRIP)
            GL.glVertex2f(y_tick_left, zero_pos + self.signal_height)
            GL.glVertex2f(y_tick_right, zero_pos + self.signal_height)
            GL.glEnd()

            # Light grey grid lines
            GL.glColor3f(0.88, 0.92, 0.92)
            GL.glBegin(GL.GL_LINE_STRIP)
            GL.glVertex2f(y_tick_left, zero_pos + self.signal_height)
            GL.glVertex2f(x_right, zero_pos + self.signal_height)
            GL.glEnd()

            # Label 1
            GL.glColor3f(0, 0, 0)
            x_pos_1 = x_left - self.label_size
            y_pos_1 = zero_pos + self.signal_height
            GL.glRasterPos2f(x_pos_1, y_pos_1)
            font = self.small_font
            label_one = "1"
            GLUT.glutBitmapCharacter(font, ord(label_one))

        # Label y axis
        text = _("Monitor Name")
        font = self.label_font
        x_pos_y_label = self.canvas_origin[0] + self.y_axis_offset / 2
        y_pos_y_label = y_top + self.y_axis_offset / 2
        GL.glColor3f(0, 0, 0)
        GL.glRasterPos2f(x_pos_y_label, y_pos_y_label)
        for character in text:
            GLUT.glutBitmapCharacter(font, ord(character))

    def draw_signal(self):
        """Draw signal traces for each monitor."""
        self.draw_grid(spin_value=self.cycles_completed)
        # e.g. if cycles period is 2, the label goes 0, 2, 4, ...
        cycle_period = self.cycles_completed \
            // (self.num_period_display - 1)
        # Draw signals one on top of another.
        if self.cycles_completed > 0:
            # Draw all signals selected
            for count in range(len(self.monitored_signal_list)):
                # Get name of monitor
                monitor_name = self.monitored_signal_list[count]
                # Add the label of monitor
                text = str(monitor_name)
                font = self.small_font
                # Put label slightly to the right
                x_pos_y_label = (
                    self.canvas_origin[0] + self.y_axis_offset
                    + self.x_grid_offset
                )
                # Grid at 0
                zero_pos = (
                    self.canvas_origin[1]
                    + self.x_axis_offset
                    + self.y_grid_offset_lower
                    + count * (self.signal_y_distance + self.signal_height)
                )
                y_pos_y_label = zero_pos + self.signal_height / 2
                GL.glColor3f(0, 0, 0)
                GL.glRasterPos2f(x_pos_y_label, y_pos_y_label)
                for character in text:
                    GLUT.glutBitmapCharacter(font, ord(character))
                # Find signal list for each monitor
                [device_id, output_id] = \
                    self.devices.get_signal_ids(monitor_name)
                signal_list = \
                    self.monitors.monitors_dictionary[(device_id, output_id)]

                # Signal trace depends on the signal count
                if count % 3 == 1:
                    # Blue
                    GL.glColor3f(
                        self.signal_colours[2][0],
                        self.signal_colours[2][1],
                        self.signal_colours[2][2],
                    )
                elif count % 3 == 2:
                    # Red
                    GL.glColor3f(
                        self.signal_colours[1][0],
                        self.signal_colours[1][1],
                        self.signal_colours[1][2],
                    )
                else:
                    # Black
                    GL.glColor3f(
                        self.signal_colours[0][0],
                        self.signal_colours[0][1],
                        self.signal_colours[0][2],
                    )
                GL.glBegin(GL.GL_LINE_STRIP)

                # Find starting y position
                # y offset is half of tick_width
                offset = (
                    count * (self.signal_height + self.signal_y_distance)
                    + self.tick_width / 2
                    + self.label_width
                )

                # Draw signal trace
                for index in range(len(signal_list)):
                    indiv_signal = signal_list[index]
                    # Horizontal start point of signal
                    if self.cycles_completed <= 10:
                        normal_cycle_width = self.signal_cycle_width
                        x_start = (
                            (index * normal_cycle_width)
                            + self.canvas_origin[0]
                            + self.x_axis_offset
                            + self.y_axis_offset
                        )
                        x_end = x_start + normal_cycle_width

                        # If signal is high
                        if indiv_signal == self.devices.HIGH:
                            # Add offset to y
                            y = (
                                self.canvas_origin[1]
                                + self.x_axis_offset
                                + self.y_grid_offset_lower
                                + self.signal_height
                                + offset
                            )
                            GL.glVertex2f(x_start, y)
                            GL.glVertex2f(x_end, y)
                        # If signal is low
                        elif indiv_signal == self.devices.LOW:
                            # Add offset to y
                            y = (
                                self.canvas_origin[1]
                                + self.x_axis_offset
                                + self.y_grid_offset_lower
                                + offset
                            )
                            GL.glVertex2f(x_start, y)
                            GL.glVertex2f(x_end, y)
                    else:
                        # Squeeze cycles together if too many cycles chosen
                        if 10 <= self.cycles_completed < 20:
                            short_cycle_width = self.signal_cycle_width / 2
                        else:
                            short_cycle_width = self.signal_cycle_width \
                                                / cycle_period
                        x_start = (
                            (index * short_cycle_width)
                            + self.canvas_origin[0]
                            + self.x_axis_offset
                            + self.y_axis_offset
                        )
                        x_end = x_start + short_cycle_width

                        # If signal is high
                        if indiv_signal == self.devices.HIGH:
                            # Add offset to y
                            y = (
                                self.canvas_origin[1]
                                + self.x_axis_offset
                                + self.y_grid_offset_lower
                                + self.signal_height
                                + offset
                            )
                            GL.glVertex2f(x_start, y)
                            GL.glVertex2f(x_end, y)
                        # If signal is low
                        if indiv_signal == self.devices.LOW:
                            # Add offset to y
                            y = (
                                self.canvas_origin[1]
                                + self.x_axis_offset
                                + self.y_grid_offset_lower
                                + offset
                            )
                            GL.glVertex2f(x_start, y)
                            GL.glVertex2f(x_end, y)

                GL.glEnd()
