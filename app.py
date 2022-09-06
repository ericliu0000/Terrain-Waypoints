import pathlib
import tkinter as tk

import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "ui.ui"

max_z = 3700


class Messages:
    """Error messages."""
    INVALID = ("#eb0b1f", "Inputs are not valid. Nothing was executed.")
    NEGATIVE = ("#eb0b1f", "Inputs must be positive. Nothing was executed.")
    OVERLAP = ("#eb0b1f", "Overlap value must be between 0 and 100%. Nothing was executed.")
    Z_FILTER = ("#eb0b1f", f"Minimum Z height must be below {max_z} feet. Nothing was executed.")
    LOW_MIN_HEIGHT = ("#ffa500", "Minimum distance is too low. Program executed, but results may be hazardous.")
    OK_GRAPH = ("#000", "Graph generated successfully.")
    OK_EXPORT_FT = ("#000", "Exporting to feet completed successfully to path: ")
    OK_EXPORT_LL = ("#000", "Exporting to latitude/longitude completed successfully to path: ")


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

    def run(self):
        self.mainwindow.mainloop()

    def handle(self, widget_id):
        # Clear out previous error messages
        self.builder.get_object("message").configure(text="")

        try:
            check = 0
            for label in self.labels:
                check += float(self.builder.get_object(label).get())
                print(label)
        except ValueError as e:
            self.builder.get_object("message").configure(foreground="#eb0b1f", text="Inputs invalid, nothing was done")
        # self.builder.get_object("message").configure(foreground="#000")
        # self.builder.get_object("message").configure(text=str(self.count))
        # Validate all inputs

        print(widget_id)
        print(self.builder.get_object("frame_h").get())


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    app = UiApp(root)
    app.run()
