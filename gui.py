from tkinter import *
from tkinter import ttk

class orbitalParadoxGui:

    def __init__(self):
        self.root = Tk()
        self.root.title("Orbital Paradox")

        self.make_layout()

    def make_layout(self):
        height_lbl = ttk.Label(self.root, text = "Starting height of the satellite: ")
        height_txt = StringVar()
        height = ttk.Entry(self.root, textvariable = height_txt)
        
        height_lbl.grid(row = 0, column = 0,  sticky = "nwse", padx = 5, pady = 5)
        height.grid(row = 0, column = 1,  sticky = "nwse", padx = 5, pady = 5)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    gui = orbitalParadoxGui()
    gui.run()