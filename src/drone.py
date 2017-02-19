class Drone:

    def __init__(self, simulation):
        self.simulation = simulation
        self.location = [simulation.warehouses_location[0][0], simulation.warehouses_location[0][1]]
        self.payload = 0
        self.items = [0 for k in self.simulation.n_product_types]
        self.task_list = []

    def load(self, warehouse_id, item_id, quantity):
        # if drone not at warehouse location
        if self.location[0] != self.simulation.warehouses_location[warehouse_id][0] or self.location[1] != self.simulation.warehouses_location[warehouse_id][1]:
            # plan to move to warehouse then load
            self.task_list.append()

    def deliver(self, customer_id, item_id, quantity):
        pass

    def update(self):
        pass

class TaskGoTo:
    def __init__(self, y, x):
        self.y = y
        self.x = x
    def update(self, drone):
        pass