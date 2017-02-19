from src import simulation

simulation = simulation.Simulation()
simulation.extractData("../inputs/test.in")

print(simulation.getOutput())