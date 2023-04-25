# tcg cart-optimizer

A shopping optimizer for equivalent products shipped from different sellers, written in python

The aim is to minimize costs by correctly selecting which products to buy from which seller and in what quantities

The example used is the case of trading cards, but it can be applied to any context where products are equivalent regardless of their seller

## How does it work

Using the [pulp](https://github.com/coin-or/pulp) python library, it builds a linear programming model with an objective function to minimize and solves it (when feasible)

## How to try it

Look at `optimizer_test.py` file for example inputs
