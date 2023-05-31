# IC-Optimization
This repository contains code for a generalized version of a classic inventory control optimization problem presented in the book Dynamic Programming and Optimal Control by Dimitris Bertsekas.
 
 ## Model Description
This is a classic inventory control problem. We assume we are planning for a finite horizon (i.e., a finite number of time steps). In each time step, the inventory manager has to decide how many units of stock to buy based on the current stock levels. We can characterize the probability distribution of the demand using a general distribution, and we can use the backwards induction algorithm to minimize the expected long term cost and find and optimal control policy. 

### Cost-To-Go
We assume that the cost is quadratic with respect to excess demand or excess inventory. If we let $x_k$ be the stock in time $k$, $u_k$ the amount of stock that the inventory manager orders and $w_k$ the demand on time $k$, the cost is given by:

$$
g(x_k, u_k, w_k)=(x_k+u_k-w_k)^2
$$

The goal of the optimal control algorithm is to recursively optimize this cost by taking the expectation with respect to $w_k$.

## Code Tutorial

### Getting the Optimal Control Policy
```
from ICBackwardsInduction import InventoryControlSolver

# Inputs
time_horizon= 61
max_stock= 10
terminal_cost= [0 for k in range(max_stock+1)]
demand_dist= [0, 0, 0, 0, 0, 0.25, 0.025, 0.05, 0.05, 0.20, 0.20, 0.05, 0.05, 0.05, 0.025, 0.025, 0.025]

# Run Optimal Control Algorithm
# Define model
model= InventoryControlSolver(time_horizon, max_stock, terminal_cost, demand_dist)

# Solve Backwards Induction
policy, cost= model.fit()
```

### Running a Simulation
The modular implementation also enables you to run simulations. This help you to see how would your algorithm perform in the real world assuming that the demand is randoml determined by the probability distribution that you initially provided. 
```
demand= model.GenDemand()
sim_data= model.Simulation(demand=demand, initial_stock=0)
```
