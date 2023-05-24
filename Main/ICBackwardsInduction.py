#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 18 18:20:30 2023
Dynamic Programing Test
@author: fernandoacosta-perez
"""

import numpy as np
import pandas as pd

class InventoryControlSolver:
    def __init__(self, time_horizon, max_stock, terminal_cost, demand_dist):
        """

        Parameters
        ----------
        time_horizon : For how many periods are we optimizing?
        
        max_stock : What is the maximum stoc that we can hold at a particular time?
            
        demand_dist : What is the demand distribution? 
            Dtype: a list with fractions taht sum to one. Element i of the list 
                   correspond to having a demand of i
        Returns
        -------
        None.

        """
        
        self.time_horizon= time_horizon
        self.max_stock= max_stock
        self.terminal_cost= terminal_cost
        self.demand_dist= demand_dist


    def solve_subproblem(self, x, tcost):
        """
        Parameters
        ----------
        x : A number denoting the current state for which we are optimizing
        
        
        tcost : It is a vector that for each possible action, contains the 
        cost that would be incured in the next period by taking this action
    
        Returns
        -------
        action: for a given state and time, it gives the optimal action
        
        cost: for a given state and time, it gives the expected cost
        """
        
        optimal_action= None
        optimal_cost= None
        
        for i in range((self.max_stock-x)+1):        
            # Calculate expected cost
            exp_cost= sum([self.demand_dist[l]*(i +(x+i-l)**2 + tcost[max(0, x+i-l)]) for l in range(len(self.demand_dist))])
                          
            # Determine Optimality
            if optimal_cost == None:
                optimal_action= i
                optimal_cost= exp_cost
                
            elif (exp_cost < optimal_cost):
                optimal_action= i
                optimal_cost= exp_cost
                
        return optimal_action, optimal_cost
    
    def fit(self):
        """
        Returns
        -------
        policy_matrix : A matrix for the optimal action for each possible state-time pair
        
        j : The expected cost for each possible state-time pair
        """
        
        j= [self.terminal_cost]
        policy_matrix= []
        
        for k in range(self.time_horizon):
            utcost= []
            control= []
            for state in range(self.max_stock+1):
                # Solve system
                action, cost= self.solve_subproblem(state, j[k])
                
                # Append Data 
                utcost.append(cost)
                control.append(action)
                
            # Append Values to General List
            j.append(utcost)
            policy_matrix.append(control)
            
        # Transform to numpy array and return
        j= np.array(j[1:]) # remove the first row that contains the terminal cost
        policy_matrix= np.flip(np.array(policy_matrix), axis=0)
        
        # Globalize Policy Matrix
        self.policy_matrix= policy_matrix
        
        return policy_matrix, j
    
    def GenDemand(self):
        """

        Returns
        -------
        demand: simulation of the demand

        """
        
        demand= np.random.choice(np.arange(0, len(self.demand_dist)), p=self.demand_dist, size= (self.time_horizon,))
        
        return demand
    
    def Simulation(self, demand, initial_stock):
        """
        Parameters
        ----------
        demand : list of demand points 

        Returns
        -------
        None.

        """
        
        action_log= []
        stock_log= []
        unmet_log= []
        
        # Set Intial Action
        stock= initial_stock
        
        for k in range(len(demand)):
            
            # How Much to Buy?

            action= self.policy_matrix[k, stock]
            action_log.append(action)
            
            # Stock at the end of the period
            stock= stock+action
            
            # Calculate and Save Unmet Demand
            unmet_log.append(stock-demand[k])
            
            # Stock When the Demand Comes
            stock= max(0, stock-demand[k])
            stock_log.append(stock)
            
        # Build Data Set
        data= pd.DataFrame()
        
        # Populate Data
        data['Time']= [i for i in range(len(demand))]
        data['Action']= action_log
        data['Stock']= stock_log
        data['Demand']= demand
        data['UD-Loss']= unmet_log
        
        # Reshape Data
        data= pd.melt(data, id_vars= ['Time'])
        self.data= data
        
        return self.data

    def GetAnimationData(self):
        
        
        animation_data= pd.DataFrame(columns= list(self.data)+['Frame'])
        frames= [i for i in range(self.time_horizon)]
        
        for frame in frames:
            
            # Define Frame Data 
            frame_idx= self.data['Time'] <= frame
            frame_data= self.data[frame_idx].copy()
            frame_data['Frame']= np.full(sum(frame_idx), fill_value= frame)
            
            # Build Dataset
            animation_data= pd.concat((animation_data, frame_data), axis=0)
        
        return animation_data
    
        
        

# Test Main Algorithm
# Test 1
# time_horizon= 3
# max_stock= 3
# terminal_cost= [0, 0, 0, 0]
# demand_dist= [0, 0.10, 0.70, 0.20]

# Test 2
time_horizon= 61
max_stock= 10
terminal_cost= [0 for k in range(max_stock+1)]
demand_dist= [0, 0, 0, 0, 0, 0.25, 0.025, 0.05, 0.05, 0.20, 0.20, 0.05, 0.05, 0.05, 0.025, 0.025, 0.025]

# Define model
model= InventoryControlSolver(time_horizon, max_stock, terminal_cost, demand_dist)

# Solve Backwards Induction
policy, cost= model.fit()

# Generate Simulated Demand
demand= model.GenDemand()

# Run Simulation and Get Data
sim_data= model.Simulation(demand=demand, initial_stock=0)


an_data= model.GetAnimationData()
