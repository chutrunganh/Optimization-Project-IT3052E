import random as rm

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
    for v in range(k):
        if sum_quant[v]>upper(v) or sum_quant[v]<lower(v):
            violation += 1 
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
        return rm.choice(candidate)
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
            sum_cost=[0 for i in range(k)]
            for i in range(n):
                sum_cost[X[i]]+=cost(i)
            total_cost=0
            for i in range(k):
                if can_go(i):
                    total_cost+=sum_cost[i]
            print(total_cost)
            print('Solution found!')
            break
        
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

import time 
start=time.time()
if __name__ == '__main__':
    with open("input.txt", 'r') as file:
         input_lines = [line.strip() for line in file]
    lst=[]
    for x in input_lines:
        lst.append(str(x).split())
    N=int(lst[0][0])
    K=int(lst[0][1])
    orders =[]
    vehicles =[]
    for o in range(N):
        orders .append([int(i) for i in lst[o+1]])
    for v in range(K):
        vehicles .append([int(j) for j in lst[v+N+1]])
    #Random
    X=[-1 for i in range(N)]
    for i in range(N):
        X[i]=rm.randint(0,K-1)
    local_search(2000,N,K,orders,vehicles,X)
finish=time.time()
print(finish-start)



       
        
