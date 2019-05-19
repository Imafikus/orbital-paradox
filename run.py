from op import OrbitalParadox
from simulation import Simulation

def main():    
    op = OrbitalParadox()
    time_period = op.C_SECONDS_IN_YEAR / 500
    op.main_loop(time_period, True, False)

    sim = Simulation()

    x, y = op.get_coordinates_arrays()
    x, y = sim.compress_arrays(x, y)
    x, y = sim.arrays_scaled_to_fit_screen(x, y)

    sim.start_loop(x, y)

if __name__ == "__main__":
    main()
    