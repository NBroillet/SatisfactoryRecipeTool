#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 11:40:48 2019

@author: Nicolas Broillet
@version : 0.1
"""
import math

# Supposition : smelter at 60 items/min,and no overclocking

class Recipe:
    def __init__(self, name, outputPerMin, listRequired, machine):
        self.name = name
        self.outputPerMin = outputPerMin
        self.listRequired = listRequired
        self.machine = machine
        
class Requirement:
    def __init__(self, recipe, inputNeeded):
        self.recipe = recipe
        self.inputNeeded = inputNeeded
        
class Machine:
    def __init__(self, name):
        self.name = name

#------------------------------------------------------------------------------
# Tier 0
#------------------------------------------------------------------------------
ironOre = Recipe('iron ore', 60, [], Machine('Miner'))
copperOre = Recipe('copper ore', 60, [], Machine('Miner'))
limestoneOre = Recipe('limestone ore', 60, [], Machine('Miner'))

#------------------------------------------------------------------------------
# Tier 1
#------------------------------------------------------------------------------
ironIngot = Recipe('iron ingot', 30, [Requirement(ironOre, 30)], Machine('Smelter'))
copperIngot = Recipe('copper ingot', 30, [Requirement(copperOre, 30)], Machine('Smelter'))
concrete = Recipe('concrete', 15, [Requirement(limestoneOre, 45)], Machine('Constructor'))

#------------------------------------------------------------------------------
# Tier 2
#------------------------------------------------------------------------------
ironPlate = Recipe('iron plate', 15, [Requirement(ironIngot, 30)], Machine('Constructor'))
ironRod = Recipe('iron rod', 15, [Requirement(ironIngot, 15)], Machine('Constructor'))
wire = Recipe('wire', 45, [Requirement(copperIngot, 15)], Machine('Constructor'))

#------------------------------------------------------------------------------
# Tier 3
#------------------------------------------------------------------------------
screw = Recipe('screw', 90, [Requirement(ironRod, 15)], Machine('Constructor'))
cable = Recipe('cable', 15, [Requirement(wire, 30)], Machine('Constructor'))

#------------------------------------------------------------------------------
# Tier 4
#------------------------------------------------------------------------------
reinforcedIronPlate = Recipe('reinforced iron plate', 5, [Requirement(screw, 120), Requirement(ironPlate, 20)], Machine('Assembler'))
rotor = Recipe('rotor', 6, [Requirement(ironRod, 18), Requirement(screw, 132)], Machine('Assembler'))

#------------------------------------------------------------------------------
# Tier 4
#------------------------------------------------------------------------------
modularFrame = Recipe('modular frame', 4, [Requirement(reinforcedIronPlate, 12), Requirement(ironRod, 6)], Machine('Assembler'))


#------------------------------------------------------------------------------
# Requests
#------------------------------------------------------------------------------

def request(recipe, quantityPerMin, leaves):
    print('Item choosen : ' + str(quantityPerMin) + ' ' + recipe.name + ' per min')
    ratio = quantityPerMin / recipe.outputPerMin
    for required in recipe.listRequired:
        recursiveRequest(required, ratio, leaves, 1)
    print('----------------------------------------')
    
def recursiveRequest(required, ratio, leaves, printLevel):
    nbNeeded = ((ratio * required.inputNeeded) / required.recipe.outputPerMin) * required.recipe.outputPerMin
    #nbMachineNeeded = quarter(nbNeeded/required.recipe.outputPerMin)
    nbMachineNeeded = (nbNeeded/required.recipe.outputPerMin)
    
    print('   ' * printLevel + required.recipe.name + ' : ' + str(nbNeeded) + ' (' + str(nbMachineNeeded) + ' ' + required.recipe.machine.name + ')')
    
    for subRequired in required.recipe.listRequired:
        if(subRequired.recipe in leaves):
            #print('   ' * printLevel + 'leaf')
            print()
        else:
            recursiveRequest(subRequired, nbMachineNeeded, leaves, printLevel+1)

# Round up to the nearest multiple of 0.25
def quarter(x):
    return math.ceil(x*4)/4

def main():
    # By default, the algorithm will continue until the very first elements but will not include the cost of the miner(s)
    # To stop the tree searching to a certain point, add it in the leaves list
    leaves = [ironOre, copperOre, limestoneOre]
    request(rotor, 6, leaves)
    
    request(modularFrame, 4, leaves)
    request(modularFrame, 8, leaves)

main()