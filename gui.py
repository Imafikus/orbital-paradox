from tkinter import *
from tkinter import ttk, messagebox
import check_types as ct
import op
from simulation import Simulation

class orbitalParadoxGui:

    #? satellite surfaces approximations, all given in m2
    SAT_SURFACES_DICT = {
        "ISS": 74 * 110, 
        "Hubble": 13.2 * 4.2, 
        "Voyager": 4 * 4,
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

        
        #? height widget
        height_lbl = ttk.Label(self.root, text = "Starting height of the satellite (m): ")
        self.height_txt = StringVar()
        height = ttk.Entry(self.root, textvariable = self.height_txt)

        height_lbl.grid(row = 0, column = 0,  sticky = "nwse", padx = 5, pady = 5)
        height.grid(row = 0, column = 1,  sticky = "nwse", padx = 5, pady = 5)

        #? time_period widget
        time_period_lbl = ttk.Label(self.root, text = "Time period for the simulation (s): ")
        self.time_period_txt = StringVar()
        time_period = ttk.Entry(self.root, textvariable = self.time_period_txt)

        time_period_lbl.grid(row = 1, column = 0,  sticky = "nwse", padx = 5, pady = 5)
        time_period.grid(row = 1, column = 1,  sticky = "nwse", padx = 5, pady = 5)

        #? cd widget
        cd_lbl = ttk.Label(self.root, text = "Starting cd of the satellite: ")
        self.cd_txt = StringVar()
        cd = ttk.Entry(self.root, textvariable = self.cd_txt)

        cd_lbl.grid(row = 2, column = 0,  sticky = "nwse", padx = 5, pady = 5)
        cd.grid(row = 2, column = 1,  sticky = "nwse", padx = 5, pady = 5)

        #? satellite widget
        satellites_lbl = ttk.Label(self.root, text = "Choose satellite for the simulation: ")        
        self.satellite_txt = StringVar()
        satellites = ttk.Combobox(self.root, textvariable = self.satellite_txt, state = "readonly")
        satellites["values"] = self.SAT_NAMES
        satellites.current(0)

        satellites_lbl.grid(row = 5, column = 0,  sticky = "nwse", padx = 5, pady = 5)
        satellites.grid(row = 5, column = 1,  sticky = "nwse", padx = 5, pady = 5)

        #? start button widget
        start_button = ttk.Button(self.root, text = "Start Simulation", command = self.start_simulation)
        start_button.grid(row = 7, rowspan = 2, column = 0, columnspan = 2, sticky = "nwse", padx = 5, pady = 5)

    def run(self):
        self.root.mainloop()
    
    def start_simulation(self):
        """
        Gets the params from the input fields and starts the simulation if the input is correct
        """
        print("start_simulation")

        height = self.height_txt.get()
        print("height val: ", height)

        time_period = self.time_period_txt.get()
        print("time period: ", time_period)
        
        cd = self.cd_txt.get()
        print("cd: ", cd)

        sat_name = self.satellite_txt.get()
        print("Satellite name: ", sat_name)
        print("Satellite surface: ", self.SAT_SURFACES_DICT[sat_name])

        error_message = self.check_input(height, time_period, cd)
        if error_message:
            messagebox.showerror(message = error_message, title="Invalid input", icon = "error")
            return
        
        sim = op.OrbitalParadox()
        sim.set_h(float(height))
        sim.set_C_Cd(float(cd))
        sim.set_C_Area(float(self.SAT_SURFACES_DICT[sat_name]))

        print(type(sim.get_h()))

        sim.main_loop(int(time_period), include_drag_force = True)
        
        #? remove window after the simulation starts 
        self.root.destroy()

        animate = Simulation()
        x, y = sim.get_coordinates_arrays()
        animate.start_loop(x, y)
        
        sim.plot_coordinates()
        sim.plot_height_through_time()
        sim.plot_speed_through_time()

    def check_input(self, height, time_period, cd):
        """
        Check for the incorrect input.

        Return error_message, if message is empty, there were no mistakes
        """

        error_message = ""

        if not ct.check_positive_float(height):
                error_message += "Height must be positive float.\n"
        
        if not ct.check_positive_int(time_period):
            error_message += "Time period must be positive int.\n"
        
        if not ct.check_positive_float(cd):
            error_message += "Drag coef. must be positive float.\n"
        
        
        return error_message


if __name__ == "__main__":
    gui = orbitalParadoxGui()
    gui.run()
    