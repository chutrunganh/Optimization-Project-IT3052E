# Bin Packing Problem

## Problem Statement

The bin packing problem is an optimization problem in which items of different sizes must be packed into a finite number of bins or containers, each having a
fixed given capacity, in a way that optimizes the problem depending on the desired outcome.

The goal in this case:

1) An “item” is packed to at most 1 “bin”;
2) Each “bin” must meet the requirements of loaded
quantities: a lower bound & an upper bound;
3) The profit gained from “packed items” is maximal.

Data provided:

- K number of vehicles/bins
- N number of items/orders. Each item has a weight (w) and a profit (p)
- Lower bound (c1) and upper bound (c2) of each vehicle

For more explanation, problem modeling and implementation, please refer to our [report](https://github.com/chutrunganh/Optimization-Project-IT3052E/blob/main/Group-5-Bin-packing-problem.pdf)

## Solution

We have implemented a solution for the bin packing problem using the following algorithms:

1. Integer Linear Programming (ILP)
2. Constraint Programming (CP)
3. "Greedy" assigning method
4. Local search algorithm for completion

## Results

![Results](/result.png)

