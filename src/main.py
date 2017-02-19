from src import simulation
from src import solver_example

solver = solver_example.SolverExample(0, 10)
sim = simulation.Simulation(solver)
sim.extractData("../inputs/test.in")
sim.simulate()

with open("../outputs/test.txt", 'w') as file:
    file.write(sim.getOutput())