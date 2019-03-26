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
ironOre = Recipe('iron ore', 60, [])
copperOre = Recipe('copper ore', 60, [])
limestoneOre = Recipe('limestone ore', 60, [])

#------------------------------------------------------------------------------
# Tier 1
#------------------------------------------------------------------------------
ironIngot = Recipe('iron ingot', 30, [Quantity(ironOre, 30)])
copperIngot = Recipe('copper ingot', 30, [Quantity(copperOre, 30)])
concrete = Recipe('concrete', 15, [Quantity(limestoneOre, 45)])

#------------------------------------------------------------------------------
# Tier 2
#------------------------------------------------------------------------------
ironPlate = Recipe('iron plate', 15, [Quantity(ironIngot, 30)])
ironRod = Recipe('iron rod', 15, [Quantity(ironIngot, 15)])
wire = Recipe('wire', 45, [Quantity(copperIngot, 15)])

#------------------------------------------------------------------------------
# Tier 3
#------------------------------------------------------------------------------
screw = Recipe('screw', 90, [Quantity(ironRod, 15)])
cable = Recipe('cable', 15, [Quantity(wire, 30)])

#------------------------------------------------------------------------------
# Tier 4
#------------------------------------------------------------------------------
reinforcedIronPlate = Recipe('reinforced iron plate', 5, [Quantity(ironRod, 120), Quantity(ironPlate, 20)])
rotor = Recipe('rotor', 6, [Quantity(ironRod, 18), Quantity(screw, 22)])

#------------------------------------------------------------------------------
# Tier 4
#------------------------------------------------------------------------------
modularFrame = Recipe('modular frame', 4, [Quantity(reinforcedIronPlate, 12), Quantity(ironRod, 6)])

#------------------------------------------------------------------------------

def main():
    print()

main()