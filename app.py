import pathlib
import tkinter as tk

import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "ui.ui"

max_z = 3700

class Messages:
    """Message tiers"""
    ERROR = "#eb0b1f"
    WARN = "#ffa500"
    OK = "000"
    """Message values"""
    INVALID = (ERROR, "Inputs are not valid. Nothing was executed.")
    NEGATIVE = (ERROR, "Inputs must be positive. Nothing was executed.")
    OVERLAP = (ERROR, "Overlap value must be between 0 and 100%. Nothing was executed.")
    Z_FILTER = (ERROR, f"Minimum Z height must be below {max_z} feet. Nothing was executed.")
    LOW_MIN_HEIGHT = (WARN, "Minimum distance is too low.", " Program executed, but results may be undesirable.")
    OK_GRAPH = (OK, "Graph generated successfully.")
    OK_EXPORT_FT = (OK, "Exporting to feet completed successfully to path: ")
    OK_EXPORT_LL = (OK, "Exporting to latitude/longitude completed successfully to path: ")


class UiApp:
    count = 0
    labels = []

    def __init__(self, master=None, translator=None):
        self.builder = builder = pygubu.Builder(translator)
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("frame1", master)
        builder.connect_callbacks(self)

        for name, obj in self.builder.objects.items():
            if type(obj) == pygubu.plugins.ttk.ttkstdwidgets.TTKEntry:
                self.labels.append(name)

        self.builder.get_object("message").configure(text="")

    def run(self):
        self.mainwindow.mainloop()

    def handle(self, widget_id):
        # Clear out previous error messages and set persistent message variable
        self.builder.get_object("message").configure(text="")
        color, message = Messages.OK, ""

        labels = {}

        # Check that inputs are numbers
        try:
            check = 0
            for label in self.labels:
                val = float(self.builder.get_object(label).get())
                # Check that numbers are in bounds
                if val < 0:
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
        if labels["frame_z_filter"] > max_z:
            color, message = Messages.Z_FILTER
        if labels["frame_min_height"] < 10:
            if color != Messages.ERROR:
                color, message = Messages.LOW_MIN_HEIGHT[0], Messages.LOW_MIN_HEIGHT[1] + Messages.LOW_MIN_HEIGHT[2]
            else:
                message += " " + Messages.LOW_MIN_HEIGHT[1]

        # If error, exit this function
        if color == Messages.ERROR:
            self.builder.get_object("message").configure(foreground=color, text=message)
            return

        # TODO: handle button events
        match widget_id:
            case "graph":
                color, message = Messages.OK_GRAPH
            case "export_ft":
                color, message = Messages.OK_EXPORT_FT
            case "export_ll":
                color, message = Messages.OK_EXPORT_LL

        self.builder.get_object("message").configure(foreground=color, text=message)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    app = UiApp(root)
    app.run()
