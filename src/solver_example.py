import math


class SolverExample:
    def __init__(self, min_score_to_deliver, factor_picking_item):
        self.min_score_to_deliver = min_score_to_deliver
        self.factor_picking_item = factor_picking_item

    def init_solver(self, simulation):
        self.simulation = simulation

    def solve_turn(self):
        for drone in self.simulation.drones:
            if drone.is_free():
                # look for worthy deliveries with current payload
                scores = []
                for i_order, order_items in enumerate(self.simulation.orders_items):
                    order_location = self.simulation.orders_location[i_order]
                    order_y = order_location[0]
                    order_x = order_location[1]
                    order_distance = drone.get_distance_to(order_y, order_x)
                    deliverable_items = [min(drone.items[item_id], order_items[item_id]) for item_id in range(self.simulation.n_item_types)]
                    scores.append(
                        sum([1000. / deliverable_item if deliverable_item > 0 else 0 for deliverable_item in deliverable_items]) / order_distance)
                best_score = max(scores)
                best_score_id = scores.index(best_score)
                best_order_items = self.simulation.orders_items[best_score_id]
                best_deliverable_items = [min(drone.items[item_id], best_order_items[item_id]) for item_id in range(self.simulation.n_item_types)]
                if best_score > self.min_score_to_deliver:
                    for item_id, quantity in enumerate(best_deliverable_items):
                        if quantity > 0:
                            drone.deliver(best_score_id, item_id, quantity)
                # look for worthy deliveries around closest warehouse
                else:
                    warehouses_distance = [drone.get_distance_to(warehouse_location[0], warehouse_location[1]) if sum(
                        self.simulation.warehouses_items[warehouse_id]) > 0 else math.inf for warehouse_id, warehouse_location in
                                           enumerate(self.simulation.warehouses_location)]
                    closest_warehouse_id = warehouses_distance.index(min(warehouses_distance))
                    closest_warehouse_location = self.simulation.warehouses_location[closest_warehouse_id]
                    closest_warehouse_y = closest_warehouse_location[0]
                    closest_warehouse_x = closest_warehouse_location[1]
                    closest_warehouse_items = self.simulation.warehouses_items[closest_warehouse_id]
                    scores = []
                    order_quantity_items = []
                    for i_order, order_items in enumerate(self.simulation.orders_items):
                        order_location = self.simulation.orders_location[i_order]
                        order_y = order_location[0]
                        order_x = order_location[1]
                        order_distance = math.sqrt((closest_warehouse_y - order_y) ** 2 + (closest_warehouse_x - order_x) ** 2)
                        quantity_items = []
                        for item_id in range(self.simulation.n_item_types):
                            quantity = 0
                            while drone.payload + (quantity + 1) * self.simulation.product_weights[
                                item_id] <= self.simulation.max_payload and quantity < \
                                    closest_warehouse_items[item_id]:
                                quantity += 1
                            quantity_items.append(quantity)
                        order_quantity_items.append(quantity_items)
                        scores.append(
                            sum([quantity_items[item_id] * self.factor_picking_item + 1000. / order_items[item_id] if order_items[item_id] > 0 else 0
                                 for item_id in range(self.simulation.n_item_types)]) / order_distance)
                    best_score = max(scores)
                    best_score_id = scores.index(best_score)
                    best_quantity_items = order_quantity_items[best_score_id]
                    payload_simulation = drone.payload
                    quantity_to_load_items = [0 for k in range(self.simulation.n_item_types)]
                    for quantity in range(1, max(best_quantity_items) + 1):
                        item_id_of_quantity = [item_id for item_id, item_quantity in enumerate(best_quantity_items) if quantity == item_quantity]
                        utilities = []
                        for item_id in item_id_of_quantity:
                            utilities.append(sum(order_items[item_id] for order_items in self.simulation.orders_items))
                        for k in range(len(utilities)):
                            max_utility_id = utilities.index(max(utilities))
                            item_id = item_id_of_quantity[max_utility_id]
                            simulated_quantity = quantity
                            while simulated_quantity > 0:
                                if payload_simulation + simulated_quantity * self.simulation.product_weights[item_id] <= self.simulation.max_payload:
                                    quantity_to_load_items[item_id] += simulated_quantity
                                    break
                                else:
                                    simulated_quantity -= 1
                            utilities[max_utility_id] = 0
                    for item_id, quantity_to_load in enumerate(quantity_to_load_items):
                        if quantity_to_load > 0:
                            drone.load(closest_warehouse_id, item_id, quantity_to_load)
