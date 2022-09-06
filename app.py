import tkinter as tk
import tkinter.font as tkFont


class App:
    def __init__(self, root):
        # setting title
        root.title("undefined")
        # setting window size
        width = 1280
        height = 720
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GLabel_822 = tk.Label(root)
        # ft = tkFont.Font(family='Times',size=10)
        # GLabel_822["font"] = ft
        GLabel_822["fg"] = "#333333"
        GLabel_822["justify"] = "center"
        GLabel_822["text"] = "label"
        GLabel_822.place(x=20, y=110, width=70, height=25)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
