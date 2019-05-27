from op import OrbitalParadox
from simulation import Simulation

import argparse

def main():    

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "drag",
        choices=['true', 'false'],
        help="Indicates if we are counting atmosphere drag"
    )
    parser.add_argument(
        "time_period",
        type=int,
        help="Time period for the simulation (s)"
    )

    args = parser.parse_args()

    time_period = args.time_period# 15000
    
    drag = False
    if(args.drag == "true"):
        drag = True
    
    op = OrbitalParadox()    
    op.main_loop(time_period, include_drag_force = drag)

    sim = Simulation()

    x, y = op.get_coordinates_arrays()
    x, y = sim.compress_arrays(x, y)
    x, y = sim.scale_arrays_to_fit_screen(x, y)

    sim.start_loop(x, y)

if __name__ == "__main__":
    main()
    