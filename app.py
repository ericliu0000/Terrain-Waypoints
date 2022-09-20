import pathlib
import tkinter as tk

import pygubu

import generate_waypoints

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "ui.ui"

max_z = 3700


class Messages:
    """Message colors"""
    ERROR = "#eb0b1f"
    WARN = "#eea500"
    OK = "#000"

    """Message values"""
    INVALID = (ERROR, "Inputs are not valid. Nothing was executed.")
    NEGATIVE = (ERROR, "Inputs must be positive. Nothing was executed.")
    OVERLAP = (ERROR, "Overlap value must be between 0 and 100%. Nothing was executed.")
    Z_FILTER = (ERROR, f"Minimum Z height must be below {max_z} feet. Nothing was executed.")
    LOW_MIN_HEIGHT = (WARN, "\nMinimum distance is too low. Results may be undesirable.")
    LONG_RUN_TIME = (
        WARN,
        "Requested waypoints are very close together, and run time could be long.\nPress button again to confirm.")
    OK_GRAPH = (OK, "Graph generated successfully.")
    OK_EXPORT_FT = (OK, "Exporting to feet completed successfully: ")
    OK_EXPORT_LL = (OK, "Exporting to latitude/longitude completed successfully: ")


class UiApp:
    count = 0
    labels = []
    long_run = False

    def __init__(self, master=None, translator=None):
        self.builder = builder = pygubu.Builder(translator)
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("frame1", master)
        builder.connect_callbacks(self)

        # Pull in labels from UI
        for name, obj in self.builder.objects.items():
            if type(obj) == pygubu.plugins.ttk.ttkstdwidgets.TTKEntry:
                self.labels.append(name)

        self.builder.get_object("message").configure(text="")

    def run(self):
        self.mainwindow.mainloop()

    def handle(self, widget_id):
        # Clear out previous error messages and set persistent message variable
        self.builder.get_object("message").configure(foreground=Messages.OK)
        color, message = Messages.OK, ""

        labels = {}

        # Check that inputs are numbers and in bounds
        try:
            check = 0
            for label in self.labels:
                val = float(self.builder.get_object(label).get())
                if val <= 0:
                    color, message = Messages.NEGATIVE

                labels[label] = val
                check += val
        except ValueError:
            color, message = Messages.INVALID
            self.builder.get_object("message").configure(foreground=color, text=message)
            return

        # Catch special cases of numbers
        if not 0 <= labels["frame_overlap"] <= 100:
            color, message = Messages.OVERLAP
        if labels["z_crop"] > max_z:
            color, message = Messages.Z_FILTER

        # If error, exit this function
        if color == Messages.ERROR:
            self.builder.get_object("message").configure(foreground=color, text=message)
            return

        # Transfer button info to variables and calculate frame spacing
        frame_h, camera_h, camera_v, fov = labels["frame_h"], labels["cam_h"], labels["cam_v"], labels["fov"]
        overlap, dist, z_crop = labels["frame_overlap"], labels["dist"], labels["z_crop"]

        frame_v = frame_h * camera_v / camera_h
        waypoint_h, waypoint_v = frame_h * (1 - overlap / 100), frame_v * (1 - overlap / 100)

        # Check for excessive run time and ask for confirmation
        if (waypoint_h * waypoint_v) < 20:
            if not self.long_run:
                color, message = Messages.LONG_RUN_TIME
                self.builder.get_object("message").configure(foreground=color, text=message)
                self.long_run = True
                return
            else:
                self.long_run = False

        # Set variables as configured
        generate_waypoints.CAMERA_H = waypoint_h
        generate_waypoints.CAMERA_V = waypoint_v
        generate_waypoints.CLEARANCE = dist
        generate_waypoints.Z_FILTER = z_crop

        match widget_id:
            case "graph":
                generate_waypoints.WaypointPlotter(generate_waypoints.FILE)

                color, message = Messages.OK_GRAPH
            case "export_feet":
                obj = generate_waypoints.WaypointGenerator(generate_waypoints.FILE)
                message = Messages.OK_EXPORT_FT[1] + "\n" + obj.export()

                color = Messages.OK_EXPORT_FT[0]
            case "export_latlong":
                obj = generate_waypoints.WaypointGenerator(generate_waypoints.FILE)
                message = Messages.OK_EXPORT_LL[1] + "\n" + obj.export_latlong()

                color = Messages.OK_EXPORT_LL[0]

        if labels["dist"] < 10:
            color, message = Messages.LOW_MIN_HEIGHT[0], message + Messages.LOW_MIN_HEIGHT[1]

        self.builder.get_object("message").configure(foreground=color, text=message)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x600")
    root.title("Waypoint Generator")
    root.wm_iconphoto(False, tk.PhotoImage(file="data/site.png"))
    app = UiApp(root)
    app.run()
