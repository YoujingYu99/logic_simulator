"""Draw the canvas and subsequent elements for the Graphical User Interface.
Classes:
--------
MyGLCanvas - handles all canvas drawing operations.
"""


import wx
import wx.glcanvas as wxcanvas
from OpenGL import GL, GLUT


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
    draw_signal(self): Draw signals chosen.
    update_switches(self): Update signals when switch states are changed.
    update_monitors(self): Redraw signals when monitors are updated.
    """

    def __init__(self, parent, devices, monitors):
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
        self.x_axis_length = 300
        self.y_axis_length = 1
        self.min_width = 0
        self.min_height = 0

        # Initialise variables for drawing signals
        # width, height
        canvas_width, canvas_height = self.GetClientSize()
        self.canvas_origin = [
            (canvas_width - self.min_width) / 2,
            (canvas_height - self.min_height) / 2,
        ]
        self.signal_height = 20
        self.signal_cycle_width = 15
        self.signal_y_distance = 3

        # Set monitors to be drawn
        self.devices = devices
        self.monitors = monitors
        # All switch IDs. Only uncomment when other modules ready
        # self.switch_id_list = self.devices.find_devices(self.devices.SWITCH)
        # self.switch_name_list = [
        #     self.devices.get_signal_name(x, None) for x in self.switch_IDs
        # ]
        self.switch_id_list = []
        self.switch_name_list = []
        # Uncomment when all modules ready
        # [self.monitored_signal_list,
        #  self.non_monitored_signal_list] = self.monitors.get_signal_names()
        self.monitored_signal_list = []
        self.non_monitored_signal_list = []

        # Bind events to the canvas
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.on_mouse)

    def init_gl(self):
        """Configure and initialise the OpenGL context."""
        size = self.GetClientSize()
        self.SetCurrent(self.context)
        GL.glDrawBuffer(GL.GL_BACK)
        GL.glClearColor(1.0, 1.0, 1.0, 0.0)
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

        # We have been drawing to the back buffer, flush the graphics pipeline
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
                "Canvas redrawn on paint event, size is ",
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
                    "Mouse button pressed at: ",
                    str(event.GetX()),
                    ", ",
                    str(event.GetY()),
                ]
            )
        if event.ButtonUp():
            text = "".join(
                [
                    "Mouse button released at: ",
                    str(event.GetX()),
                    ", ",
                    str(event.GetY()),
                ]
            )
        if event.Leaving():
            text = "".join(
                ["Mouse left canvas at: ", str(event.GetX()), ", ", str(event.GetY())]
            )
        if event.Dragging():
            self.pan_x += event.GetX() - self.last_mouse_x
            self.pan_y -= event.GetY() - self.last_mouse_y
            self.last_mouse_x = event.GetX()
            self.last_mouse_y = event.GetY()
            self.init = False
            text = "".join(
                [
                    "Mouse dragged to: ",
                    str(event.GetX()),
                    ", ",
                    str(event.GetY()),
                    ". Pan is now: ",
                    str(self.pan_x),
                    ", ",
                    str(self.pan_y),
                ]
            )
        if event.GetWheelRotation() < 0:
            self.zoom *= 1.0 + (event.GetWheelRotation() / (20 * event.GetWheelDelta()))
            # Adjust pan so as to zoom around the mouse position
            self.pan_x -= (self.zoom - old_zoom) * ox
            self.pan_y -= (self.zoom - old_zoom) * oy
            self.init = False
            text = "".join(
                ["Negative mouse wheel rotation. Zoom is now: ", str(self.zoom)]
            )
        if event.GetWheelRotation() > 0:
            self.zoom /= 1.0 - (event.GetWheelRotation() / (20 * event.GetWheelDelta()))
            # Adjust pan so as to zoom around the mouse position
            self.pan_x -= (self.zoom - old_zoom) * ox
            self.pan_y -= (self.zoom - old_zoom) * oy
            self.init = False
            text = "".join(
                ["Positive mouse wheel rotation. Zoom is now: ", str(self.zoom)]
            )
        if text:
            self.render(text)
        else:
            self.Refresh()  # triggers the paint event

    def render_text(self, text, x_pos, y_pos):
        """Handle text drawing operations."""
        GL.glColor3f(0.0, 0.0, 0.0)  # text is black
        GL.glRasterPos2f(x_pos, y_pos)
        font = GLUT.GLUT_BITMAP_HELVETICA_12

        for character in text:
            if character == "\n":
                y_pos = y_pos - 20
                GL.glRasterPos2f(x_pos, y_pos)
            else:
                GLUT.glutBitmapCharacter(font, ord(character))

    def draw_signal(self):
        """Draw signal traces for each monitor."""
        for count in range(len(self.monitored_signal_list)):
            monitor_name = self.monitored_signal_list[count]
            # Find signal list for each monitor
            [device_id, output_id] = self.devices.get_signal_ids(monitor_name)
            signal_list = self.monitors.monitors_dictionary[(device_id, output_id)]

            # Draw a sample signal trace
            # GL.glColor3f(0.0, 0.0, 1.0)  # signal trace is blue
            # GL.glBegin(GL.GL_LINE_STRIP)
            # for i in range(10):
            #     x = (i * 20) + 10
            #     x_next = (i * 20) + 30
            #     if i % 2 == 0:
            #         y = 75
            #     else:
            #         y = 100
            #     GL.glVertex2f(x, y)
            #     GL.glVertex2f(x_next, y)
            # GL.glEnd()

            # Signal trace is blue
            GL.glColor3f(0.0, 0.0, 1.0)
            GL.glBegin(GL.GL_LINE_STRIP)

            # Find starting y position
            offset = count * (self.signal_height + self.signal_y_distance)

            # Draw signal trace
            for index in range(len(signal_list)):
                indiv_signal = signal_list[index]
                # horizontal start point of signal
                x_start = (index * self.signal_cycle_width) + self.canvas_origin[0]
                x_end = x_start + self.signal_cycle_width

                # If signal is high
                if indiv_signal == self.devices.HIGH:
                    # Add offset to y
                    y = self.canvas_origin[1] + self.signal_height + offset
                    GL.glVertex2f(x_start, y)
                    GL.glVertex2f(x_end, y)
                # If signal is low
                if indiv_signal == self.devices.LOW:
                    # Add offset to y
                    y = self.canvas_origin[1] + offset
                    GL.glVertex2f(x_start, y)
                    GL.glVertex2f(x_end, y)

            GL.glEnd()

    def update_switches(self, devices):
        """Update signals when switches are changed."""
        self.devices = devices
        self.switch_id_list = devices.find_devices(devices.SWITCH)
        self.switch_name_list = [
            devices.get_signal_name(x, None) for x in self.switch_IDs
        ]

    def update_monitors(self, monitors):
        """Update monitors and redraw signal on canvas."""
        self.monitors = monitors
        # Uncomment when necessary
        # [self.monitored_signal_list,
        #     self.non_monitored_signal_list] = self.monitors.get_signal_names()

        if not self.monitored_signal_list:
            self.blank = True
