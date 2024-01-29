from ortools.sat.python import cp_model
import time

class Order:
    def __init__(self, order_id, quantity, cost):
        self.order_id = order_id
        self.quantity = quantity
        self.cost = cost

class Vehicle:
    def __init__(self, vehicle_id, low_capacity,up_capacity):
        self.vehicle_id = vehicle_id
        self.low_capacity = low_capacity
        self.up_capacity = up_capacity
        self.orders_vehicle_carry = []
        self.total_quantity = 0


def bin_packing_lower_upper_bound(N, K, orders, vehicles):
    model = cp_model.CpModel()
    x = {(i, j): model.NewBoolVar(f'x_{i}_{j}') for i in range(N) for j in range(K)}

    for i in range(N):
        model.Add(sum(x[(i, j)] for j in range(K)) <= 1)

    for j in range(K):
        quantity_sum = sum(orders[i].quantity * x[(i, j)] for i in range(N))
        model.Add(quantity_sum >= vehicles[j].low_capacity)
        model.Add(quantity_sum <= vehicles[j].up_capacity)
    
    model.Maximize(sum(orders[i].cost * x[(i, j)] for i in range(N) for j in range(K)))

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        m = 0
        for i in range(N):
            for j in range(K):
                if solver.Value(x[i,j]) > 0:
                    m+=1
        print(str(m)+'\n')
        
        for i in range(N):
            for j in range(K):
                if solver.Value(x[i,j]) > 0:
                    print(str(i+1) + ' ' + str(j+1)+'\n')
        
        print(f'Total cost: {solver.ObjectiveValue()}\n')



#Input
number_of_orders, number_of_vehicles = map(int, input().split())

Orders = []
for i in range(number_of_orders):
    quantity, cost = map(int, input().split())
    Orders.append(Order(i, quantity, cost))

Vehicles = []
for i in range(number_of_vehicles):
    low_capacity, up_capacity = map(int, input().split())
    Vehicles.append(Vehicle(i, low_capacity, up_capacity))

#Run
start_time = time.time()
bin_packing_lower_upper_bound(number_of_orders, number_of_vehicles, Orders, Vehicles)
end_time = time.time()
print(f'Execution time: {end_time - start_time}')