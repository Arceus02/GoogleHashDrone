import math

class Drone:

    def __init__(self, simulation):
        self.simulation = simulation
        self.location = [simulation.warehouses_location[0][0], simulation.warehouses_location[0][1]]
        self.payload = 0
        self.items = [0 for k in self.simulation.n_product_types]
        self.task_list = []

    def turnsBeforeTaskDone(self):
        if len(self.task_list) > 0:
            return self.task_list[0].turns_to_wait
        else:
            return 0

    def load(self, warehouse_id, item_id, quantity):
        # if drone not at warehouse location
        warehouse_y = self.simulation.warehouses_location[warehouse_id][0]
        warehouse_x = self.simulation.warehouses_location[warehouse_id][1]
        if self.location[0] != warehouse_y or self.location[1] != warehouse_x:
            # plan to move to warehouse then load
            self.task_list.append(TaskGoTo(self, self.location[0], self.location[1], warehouse_y, warehouse_x))
            self.task_list.append(TaskLoad(self.simulation, self, warehouse_id, item_id, quantity))

    def deliver(self, customer_id, item_id, quantity):
        pass

    def update(self):
        if len(self.task_list) > 0:
            task = self.task_list[0]
            task.update()
            if task.done:
                del self.task_list[0]

class TaskGoTo:
    def __init__(self, drone, y_start, x_start, y_end, x_end):
        self.drone = drone
        self.turns_to_wait = int(math.sqrt((y_start - y_end)**2+(x_start - x_end)**2))+1
        self.y_end = y_end
        self.x_end = x_end
        self.done = False
    def update(self):
        self.turns_to_wait -= 1
        if not self.turns_to_wait > 0:
            self.drone.location[0] = self.y_end
            self.drone.location[1] = self.x_end
            self.done = True

class TaskLoad:
    def __init__(self, simulation, drone, warehouse_id, item_id, quantity):
        self.simulation = simulation
        self.drone = drone
        self.warehouse_id = warehouse_id
        self.item_id = item_id
        self.quantity = quantity
        self.turns_to_wait = 1
        self.done = False
    def update(self):
        # check weight
        if self.simulation.product_weights[self.item_id]*self.quantity > self.simulation.max_payload:
            raise Exception("Loaded more than max payload : " + str(self.simulation.product_weights[self.item_id]*self.quantity) + " > " + str(self.simulation.max_payload))
        # check enough stock
        if self.simulation.warehouses_stocks[self.warehouse_id][self.item_id] < self.quantity:
            raise Exception("Not enough quantity of " + str(self.item_id) + " in warehouse " + str(self.warehouse_id))
        # effective load
        self.simulation.warehouses_stocks[self.warehouse_id][self.item_id] -= self.quantity
        self.drone.items[self.quantity] += self.quantity
        self.turns_to_wait = 0
        self.done = True