#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 11:40:48 2019

@author: Nicolas Broillet
@version : 0.1
"""
# Supposition : smelter at 60 items/min

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
reinforcedIronPlate = Recipe('reinforced iron plate', 5, [Requirement(ironRod, 120), Requirement(ironPlate, 20)], Machine('Assembler'))
rotor = Recipe('rotor', 6, [Requirement(ironRod, 18), Requirement(screw, 132)], Machine('Assembler'))

#------------------------------------------------------------------------------
# Tier 4
#------------------------------------------------------------------------------
modularFrame = Recipe('modular frame', 4, [Requirement(reinforcedIronPlate, 12), Requirement(ironRod, 6)], Machine('Assembler'))


#------------------------------------------------------------------------------
# Requests
#------------------------------------------------------------------------------

def request(recipe, quantityPerMin, exclusionList):
    print('Item choosen : ' + str(quantityPerMin) + ' ' + recipe.name + ' per min')
    ratio = quantityPerMin / recipe.outputPerMin
    for required in recipe.listRequired:
        recursiveRequest(required, ratio, exclusionList)
    
def recursiveRequest(required, ratio, exclusionList):
    nbNeeded = ((ratio * required.inputNeeded) / required.recipe.outputPerMin) * required.recipe.outputPerMin 
    print(required.recipe.name + ' : ' + str(nbNeeded))
    
    newRatio = nbNeeded / required.recipe.outputPerMin
    
    for subRequired in required.recipe.listRequired:
        if(subRequired.recipe in exclusionList):
            print('leaf')
        else:
            recursiveRequest(subRequired, newRatio, exclusionList)

def main():
    # By default, the algorithm will continue until the very first elements but will not include the cost of the miner(s)
    # To stop the tree searching to a certain point, add it in the inclusive limit list
    inclusiveLimitList = [ironOre, copperOre, limestoneOre]
    request(rotor, 6, inclusiveLimitList)

main()