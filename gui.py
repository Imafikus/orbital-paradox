from tkinter import *
from tkinter import ttk
import check_types as ct
import op

class orbitalParadoxGui:

    #? satellite surfaces approximations, all given in m2
    SAT_SURFACES_DICT = {
        "ISS": 74 * 110, 
        "Hubble:": 13.2 * 4.2, 
        "Voyager: ": 4 * 4,
        "Space Horizon": 4
    }
    SAT_NAMES = ("ISS", "Hubble", "Voyager", "Space Horizon")


    def __init__(self):
        self.root = Tk()
        self.root.title("Orbital Paradox")

        self.make_layout()

    def make_layout(self):
        """"
        Puts all the widgets in the grid and binds the functions to the correct actions
        """

        #? NOTE: all variables which are self.sth are that way on purpose, because 
        #? we need to access that data in the start simulation function

        #? time_period widget
        time_period_lbl = ttk.Label(self.root, text = "Time period for the simulation (s): ")
        self.time_period_txt = StringVar()
        time_period = ttk.Entry(self.root, textvariable = self.time_period_txt)

        time_period_lbl.grid(row = 1, column = 0,  sticky = "nwse", padx = 5, pady = 5)
        time_period.grid(row = 1, column = 1,  sticky = "nwse", padx = 5, pady = 5)
        
        #? height widget
        height_lbl = ttk.Label(self.root, text = "Starting height of the satellite (m): ")
        self.height_txt = StringVar()
        height = ttk.Entry(self.root, textvariable = self.height_txt)

        height_lbl.grid(row = 0, column = 0,  sticky = "nwse", padx = 5, pady = 5)
        height.grid(row = 0, column = 1,  sticky = "nwse", padx = 5, pady = 5)

        #? satellite widget
        satellites_lbl = ttk.Label(self.root, text = "Choose satellite for the simulation: ")        
        self.satellite_txt = StringVar()
        satellites = ttk.Combobox(self.root, textvariable = self.satellite_txt, state = "readonly")
        satellites["values"] = self.SAT_NAMES
        satellites.current(0)

        satellites_lbl.grid(row = 2, column = 0,  sticky = "nwse", padx = 5, pady = 5)
        satellites.grid(row = 2, column = 1,  sticky = "nwse", padx = 5, pady = 5)

        #? start button widget
        start_button = ttk.Button(self.root, text = "Start Simulation", command = self.start_simulation)
        start_button.grid(row = 5, rowspan = 2, column = 0, columnspan = 2, sticky = "nwse", padx = 5, pady = 5)

    def run(self):
        self.root.mainloop()
    
    def start_simulation(self):
        """
        Gets the params from the input fields and starts the simulation if the input is correct
        """
        print("start_simulation")

        print("height val: ", self.height_txt.get())
        print("time period: ", self.time_period_txt.get())
        
        sat_name = self.satellite_txt.get()
        print("Satellite name: ", sat_name)
        print("Satellite surface: ", self.SAT_SURFACES_DICT[sat_name])

        simulation = op.OrbitalParadox()
        simulation.main_loop(100_000, include_drag_force = True)

    # def check_input
    #     if not check_for_letters(self.name_txt.get()):
    #             error_message += "Name must be alphabetical.\n"
    #         #check email
    #         if not check_email(self.email_txt.get()):
    #             error_message += "Correct email must be given.\n"



if __name__ == "__main__":
    gui = orbitalParadoxGui()
    gui.run()
    