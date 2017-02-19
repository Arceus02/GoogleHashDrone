from src import drone

class Simulation:

    def __init___(self):
        self.turn = 0

    def extractData(self, pathToInput):
        with open(pathToInput, 'r') as file:
            lines = file.readlines()
            meta = lines[0].split(" ")
            self.n_rows = int(meta[0])
            self.n_columns = int(meta[1])
            self.n_drones = int(meta[2])
            self.n_turns = int(meta[3])
            self.max_payload = int(meta[4])
            self.n_product_types = int(lines[1])
            self.product_weights = [int(weight) for weight in lines[2].split(" ")]
            self.n_warehouses = int(lines[3])
            self.warehouses_location = []
            self.warehouses_stocks = []
            for i_warehouse in range(self.n_warehouses):
                i_line = 4+i_warehouse*2
                self.warehouses_location.append([int(k) for k in lines[i_line].split(" ")])
                self.warehouses_stocks.append([int(k) for k in lines[i_line+1].split(" ")])
            self.n_orders = int(lines[4+2*self.n_warehouses])
            self.orders_location = []
            self.orders_items = []
            for i_order in range(self.n_orders):
                i_line = 4+self.n_warehouses*2+i_order*3
                self.orders_location.append([int(k) for k in lines[i_line].split(" ")])
                self.orders_items.append([0 for k in range(self.n_product_types)])
                for item_type in lines[i_line+2].split(" "):
                    self.orders_items[i_order][int(item_type)] += 1
            self.drones = [drone.Drone(self) for k in range(self.n_drones)]

    def simulate(self):
        while self.turn < self.n_turns:
            self.solve_turn()
            for drone in self.drones:
                drone.update()
            self.turn += 1

    def solve_turn(self):
        #TODO
        pass