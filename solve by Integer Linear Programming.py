from ortools.linear_solver import pywraplp
import time

def GetInput():
    n, k = map(int, input().split()) # n: number of orders; k: number of vehicles
    Orders = [] #Orders[i][0] = w(i), Order[i][1] = p(i)
    Vehicles = []
    for i in range(n):
        w, p = map(int, input().split()) # w(i): quantity of ith order; p(i): cost (profit) of ith order
        Orders.append((w, p))
    for i in range(k):
        low, up = map(int, input().split()) #lower bound and upper bound of quantity loaded on a vehicle
        Vehicles.append((low, up))
    return n, k, Orders, Vehicles

def GetInputFromFile(filename):
    with open(filename, 'r') as f:
        n, k = map(int, f.readline().split())
        Orders = []
        Vehicles = []
        for i in range(n):
            w, p = map(int, f.readline().split())
            Orders.append((w, p))
        for i in range(k):
            low, up = map(int, f.readline().split())
            Vehicles.append((low, up))
    return n, k, Orders, Vehicles


n, k, Orders, Vehicles = GetInputFromFile('input.txt')

solver = pywraplp.Solver.CreateSolver('SCIP')

# Boolean variables: X[i, j] = state of order i in vehicle j: 1~order in vehicle; 0~order not in vehicle
X = {}
for i in range(n):
    for j in range(k):
        X[i, j] = solver.IntVar(0, 1, 'X['+str(i)+','+str(j)+']')

# Constraints:
# Each order is served by at most 1 vehicle: sum of x[i][j], i in range(k) <= 1
for i in range(n):
    c1 = solver.Constraint(0, 1)
    for j in range(k):
        c1.SetCoefficient(X[i, j], 1)

# Quantity in each vehicle has to be between lower and upper capacity:
# low <= quantity loaded <= upper
for j in range(k):
    c2 = solver.Constraint(Vehicles[j][0], Vehicles[j][1])
    for i in range(n):
        c2.SetCoefficient(X[i, j], Orders[i][0])

# Objective function: total cost(profit) is maximum
objective = solver.Objective()
for j in range(k):
    for i in range(n):
        objective.SetCoefficient(X[i, j], Orders[i][1])
objective.SetMaximization()
status = solver.Solve()


# Get results
if status == pywraplp.Solver.OPTIMAL:
    print(objective.Value())
    order_count = 0
    solution = []
    for j in range(k):
        for i in range(n):
            if X[i, j].solution_value() == 1:
                order_count += 1
                solution.append((i+1, j+1)) # print(j+1, i+1)
    print(order_count)
    #for order in solution:
        #print(*order)