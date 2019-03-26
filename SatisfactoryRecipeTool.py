#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 11:40:48 2019

@author: Nicolas Broillet
@version : 0.1
"""
# Supposition : smelter at 60 items/min

class Recipe:
    def __init__(self, name, outputPerMin, listRequired):
        self.name = name
        self.outputPerMin = outputPerMin
        self.listRequired = listRequired
        
class Quantity:
    def __init__(self, recipe, inputPerMin):
        self.recipe = recipe
        self.inputPerMin = inputPerMin

#------------------------------------------------------------------------------
# Tier 0
#------------------------------------------------------------------------------
ironOre = Recipe('ironOre', 60, [])

#------------------------------------------------------------------------------
# Tier 1
#------------------------------------------------------------------------------
ironIngot = Recipe('ironIngot', 60, [Quantity(ironOre, 60)])

#------------------------------------------------------------------------------
# Tier 2
#------------------------------------------------------------------------------
ironPlate = Recipe('ironPlate', 15, [Quantity(ironIngot, 30)])

ironRod = Recipe('ironRod', 15, [Quantity(ironIngot, 15)])

#------------------------------------------------------------------------------
# Tier 3
#------------------------------------------------------------------------------
screw = Recipe('screw', 90, [Quantity(ironRod, 15)])


#------------------------------------------------------------------------------
# Tier 4
#------------------------------------------------------------------------------
reinforcedIronPlate = Recipe('reinforcedIronPlate', 5, [Quantity(ironRod, 120), Quantity(ironPlate, 20)])

#------------------------------------------------------------------------------

def main():
    print()

main()