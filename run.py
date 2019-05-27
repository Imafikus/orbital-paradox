from op import OrbitalParadox
from simulation import Simulation

def main():    
    op = OrbitalParadox()
    time_period = op.C_SECONDS_IN_YEAR / 1000
    op.main_loop(time_period, include_drag_force = False)

    sim = Simulation()

    x, y = op.get_coordinates_arrays()

    sim.start_loop(x, y)

if __name__ == "__main__":
    main()
    