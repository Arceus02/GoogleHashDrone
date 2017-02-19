import math

class Drone:
    def __init__(self, simulation, id):
        self.simulation = simulation
        self.id = id
        self.location = [simulation.warehouses_location[0][0], simulation.warehouses_location[0][1]]
        self.payload = 0
        self.items = [0 for k in range(self.simulation.n_item_types)]
        self.tasks = []

    def turns_before_tasks_done(self):
        if len(self.tasks) > 0:
            return sum([task.turns_to_wait for task in self.tasks])
        else:
            return 0

    def is_free(self):
        return self.turns_before_tasks_done() == 0

    def get_distance_to(self, y, x):
        return int(math.sqrt((self.location[0] - y) ** 2 + (self.location[1] - x) ** 2)) + 1

    def load(self, warehouse_id, item_id, quantity):
        # if drone not at warehouse location
        warehouse_y = self.simulation.warehouses_location[warehouse_id][0]
        warehouse_x = self.simulation.warehouses_location[warehouse_id][1]
        if self.location[0] != warehouse_y or self.location[1] != warehouse_x:
            # plan to move to warehouse
            self.tasks.append(TaskGoTo(self, warehouse_y, warehouse_x))
        self.tasks.append(TaskLoad(self, warehouse_id, item_id, quantity))

    def deliver(self, order_id, item_id, quantity):
        order_y = self.simulation.orders_location[order_id][0]
        order_x = self.simulation.orders_location[order_id][1]
        if self.location[0] != order_y or self.location[1] != order_x:
            # plan to move to order
            self.tasks.append(TaskGoTo(self, order_y, order_x))
        self.tasks.append(TaskDeliver(self, order_id, item_id, quantity))

    def update(self):
        task_done = False
        while not task_done:
            if len(self.tasks) > 0:
                task = self.tasks[0]
                try:
                    task.update()
                except Exception as error:
                    print(error)
                    self.tasks.pop(0)
                if task.done:
                    self.tasks.pop(0)
                if not task.skipped:
                    task_done = True
            else:
                task_done = True

class Task:
    def __init__(self, simulation, turns_to_wait):
        self.turns_to_wait = 0
        self.done = False
        self.simulation = simulation
        self.skipped = False
    def update(self):
        self.turns_to_wait -= 1
        if not self.turns_to_wait > 0:
            self.end()
            self.done = True
            if self.to_string() != "":
                self.simulation.tasks_done[-1].append(self.to_string())
    def end(self):
        pass
    def to_string(self):
        return "NONE"

class TaskGoTo(Task):
    def __init__(self, drone, y, x):
        super().__init__(drone.simulation, int(math.sqrt((drone.location[0] - y)**2+(drone.location[1] - x)**2))+1)
        self.drone = drone
        self.y = y
        self.x = x
    def end(self):
        if self.drone.location[0] == self.y and self.drone.location[1] == self.x:
            self.skipped = True
        else:
            self.drone.location[0] = self.y
            self.drone.location[1] = self.x
    def to_string(self):
        return ""

class TaskLoad(Task):
    def __init__(self, drone, warehouse_id, item_id, quantity):
        super().__init__(drone.simulation, 1)
        self.drone = drone
        self.warehouse_id = warehouse_id
        self.item_id = item_id
        self.quantity = quantity
    def end(self):
        # check weight
        if self.simulation.product_weights[self.item_id]*self.quantity > self.simulation.max_payload:
            raise Exception("Exceeded max payload : " + str(self.simulation.product_weights[self.item_id]*self.quantity) + " > " + str(self.simulation.max_payload))
        # effective load
        self.quantity = min(self.simulation.warehouses_items[self.warehouse_id][self.item_id], self.quantity)
        self.simulation.warehouses_items[self.warehouse_id][self.item_id] -= self.quantity
        self.drone.items[self.item_id] += self.quantity
    def to_string(self):
        if self.quantity > 0:
            return str(self.drone.id) + " L " + str(self.warehouse_id) + " " + str(self.item_id) + " " + str(self.quantity)
        else:
            return ""

class TaskDeliver(Task):
    def __init__(self, drone, order_id, item_id, quantity):
        super().__init__(drone.simulation, 1)
        self.drone = drone
        self.order_id = order_id
        self.item_id = item_id
        self.quantity = quantity
    def end(self):
        # effective deliver
        self.quantity = min(self.drone.items[self.item_id], self.simulation.orders_items[self.order_id][self.item_id], self.quantity)
        self.simulation.orders_items[self.order_id][self.item_id] -= self.quantity
        self.drone.items[self.item_id] -= self.quantity
    def to_string(self):
        if self.quantity > 0 :
            return str(self.drone.id) + " D " + str(self.order_id) + " " + str(self.item_id) + " " + str(self.quantity)
        else:
            return ""