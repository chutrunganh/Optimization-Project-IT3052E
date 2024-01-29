import time
import random as rd

def local_search(maxIter,n,k,orders,vehicles,X):
    def lower(v):
        return vehicles[v][0]
    def upper(v):
        return vehicles[v][1]
    def quant(o):
        return orders[o][0]
    def cost(o):
        return orders[o][1]
    
    sum_quant=[0 for j in range(k)]#sum of quantity 
    for i in range(n):
        sum_quant[X[i]]+=quant(i)
    violation=0
    [violation := violation + 1 for v in range(k) if sum_quant[v]>upper(v) or sum_quant[v]<lower(v)]
    
    def range_change(v):
        #Range the total quantity of orders a vehicle can change
        return lower(v)-sum_quant[v],upper(v)-sum_quant[v]
    
    def can_go(v):
        #Check whether a vehicle can go 
        return range_change(v)[0]*range_change(v)[1]<=0
    
    def can_trade(v1,v2):
        #Check whether 2 vehicles are suitable for the local move
        if can_go(v1) and can_go(v2):
            return False
        if range_change(v1)[0]*range_change(v2)[1]<0 or range_change(v1)[1]*range_change(v2)[0]<0:        
            return True
        return False
    
    def choose_vehicles():
        #Randomly choose 2 vehicles which are suitable(can trade)
        candidate=[]
        for i in range(k):
            for j in range(i+1,k):
                if can_trade(i,j):
                    candidate.append((i,j))
        return rd.choice(candidate)
    
    def accept_change(v1,v2):
        #Acceptable range total quantity change
        #(+:v1,-:v2)
        r1=(range_change(v1)[0],range_change(v1)[1])
        r2=(-range_change(v2)[1],-range_change(v2)[0])
        if r1[0]<0 and r2[0]<0:
            ans=(max(r1[0],r2[0]),-1)
        elif r1[1]>0 and r2[1]>0:
            ans=(1,min(r1[1],r2[1]))
        return ans
    
    orders.append([0,0])#index-n,not in decisive variable
    def choose_orders(v1,v2,accept_change):
        #Choose 2 sets of orders of each vehicle to trade
        candidate_v1=[n]
        [candidate_v1.append(o) for o in range(n) if X[o]==v1]
        candidate_v2=[n]
        [candidate_v2.append(o) for o in range(n) if X[o]==v2]
        for i in candidate_v1:
            for j in candidate_v2:
                if -quant(i)+quant(j) in\
                range(accept_change[0],accept_change[1]+1):
                    return i,j,-quant(i)+quant(j)
    
    for it in range(maxIter):
        if violation==0:
            print('Solution found!')
            break
        print('***Step',it+1)
        v1,v2=choose_vehicles()
        ac=accept_change(v1,v2)
        ans=choose_orders(v1,v2,ac)
        #Propagation
        if ans!=None:
            pre_v1,pre_v2=can_go(v1),can_go(v2)
            if ans[0]!=n:
                X[ans[0]]=v2
            if ans[1]!=n:
                X[ans[1]]=v1
            sum_quant[v1]+=ans[2]
            sum_quant[v2]-=ans[2]
            if pre_v1!=can_go(v1):
                violation-=1
            if pre_v2!=can_go(v2):
              violation-=1
        else:
            print('Move failed!')

Orders = []
Vehicles = []
with open('input.txt', 'r') as f:
    n, k = map(int, f.readline().split())
    for i in range(n):
        w, p = map(int, f.readline().split())
        Orders.append((w, p))
    for j in range(k):
        low, up = map(int, f.readline().split())
        Vehicles.append((low, up))

start_time = time.time()
sorted_orders = sorted(enumerate(Orders), key=lambda x: x[1][0], reverse=True)
sorted_vehicles = sorted(enumerate(Vehicles), key=lambda x: x[1][0], reverse=True)

load = [0 for i in range(k)]
is_served = [False for i in range(n)]
X = [-1 for i in range(n)]

assignments = []

for j in range(k):
    vehicle_pos, cur_vehicle = sorted_vehicles[j]
    for i in range(n):
        if load[vehicle_pos] >= Vehicles[vehicle_pos][0]:
            break
        order_pos, cur_order = sorted_orders[i]
        if is_served[order_pos]:
            continue
        if load[vehicle_pos] + cur_order[0] <= Vehicles[vehicle_pos][1]:
            is_served[order_pos] = True
            load[vehicle_pos] += cur_order[0]
            assignments.append((order_pos, vehicle_pos))
for i in range(n):
    if not is_served[i]:
        assignments.append((i, -1))

for order, vehicle in assignments:
    X[order] = vehicle

local_search(20000, n, k, Orders, Vehicles, X)

end_time = time.time()
order_count = 0
profit = 0

for i in range(n):
    if X[i] != -1:
        order_count += 1
        profit += Orders[i][1]
print(order_count)
print(profit)
print(end_time - start_time)