#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 11:40:48 2019

@author: Nicolas Broillet
@version : 0.2
"""

# Supposition : no overclocking
class Craft:
    def __init__(self, name):
        self.name = name
        self.recipes = []
    def addRecipe(self, recipe):
        self.recipes.append(recipe)

# time per cycle in seconds
class Recipe:
    def __init__(self, linkedCraft, outputPerCycle, timePerCycle, listRequirement, machine, ticksByHand):
        self.linkedCraft = linkedCraft
        self.outputPerCycle = outputPerCycle
        self.timePerCycle = timePerCycle
        self.listRequirement = listRequirement
        self.machine = machine
        self.ticksByHand = ticksByHand
        
class Requirement:
    def __init__(self, craft, inputPerCycle):
        self.craft = craft
        self.inputPerCycle = inputPerCycle
        
#------------------------------------------------------------------------------
# Machines
#------------------------------------------------------------------------------
equipmentWorkshop = Craft('Equipment workshop')
portableMiner = Craft('Portable Miner')
miner = Craft('Miner')
smelter = Craft('Smelter')
constructor = Craft('Constructor')
assembler = Craft('Assembler')

#------------------------------------------------------------------------------
# Tier 0
#------------------------------------------------------------------------------
ironOre = Craft('Iron ore')
ironOre.addRecipe(Recipe(ironOre, 1, 1, [], miner, 1))

copperOre = Craft('Copper ore')
copperOre.addRecipe(Recipe(ironOre, 1, 1, [], miner, 1))

limestoneOre = Craft('Limestone ore')
limestoneOre.addRecipe(Recipe(limestoneOre, 1, 1, [], miner, 1))

#------------------------------------------------------------------------------
# Tier 1
#------------------------------------------------------------------------------
ironIngot = Craft('Iron ingot')
ironIngot.addRecipe(Recipe(ironIngot, 1, 2, [Requirement(ironOre, 1)], smelter, 2))

copperIngot = Craft('Copper ingot')
copperIngot.addRecipe(Recipe(copperIngot, 1, 2, [Requirement(copperOre, 1)], smelter, 2))

concrete = Craft('Concrete')
concrete.addRecipe(Recipe(concrete, 1, 4, [Requirement(limestoneOre, 3)], constructor, 1))

#------------------------------------------------------------------------------
# Tier 2
#------------------------------------------------------------------------------
ironPlate = Craft('Iron plate')
ironPlate.addRecipe(Recipe(ironPlate, 1, 4, [Requirement(ironIngot, 2)], constructor, 1))

ironRod = Craft('Iron rod')
ironRod.addRecipe(Recipe(ironRod, 1, 4, [Requirement(ironIngot, 1)], constructor, 1))

wire = Craft('Wire')
wire.addRecipe(Recipe(wire, 3, 4, [Requirement(copperIngot, 1)], constructor, 1))

#------------------------------------------------------------------------------
# Tier 3
#------------------------------------------------------------------------------
screw = Craft('Screw')
screw.addRecipe(Recipe(screw, 6, 4, [Requirement(ironRod, 1)], constructor, 2))

cable = Craft('Cable')
cable.addRecipe(Recipe(cable, 1, 4, [Requirement(wire, 2)], constructor, 1))

#------------------------------------------------------------------------------
# Tier 4
#------------------------------------------------------------------------------
reinforcedIronPlate = Craft('Reinforced iron plate')
reinforcedIronPlate.addRecipe(Recipe(reinforcedIronPlate, 1, 12, [Requirement(ironPlate, 4), Requirement(screw, 24)], assembler, 3))

rotor = Craft('Rotor')
rotor.addRecipe(Recipe(rotor, 1, 10, [Requirement(ironRod, 3), Requirement(screw, 22)], assembler, 3))

#------------------------------------------------------------------------------
# Tier 4
#------------------------------------------------------------------------------
modularFrame = Craft('Modular frame')
modularFrame.addRecipe(Recipe(modularFrame, 1, 15, [Requirement(reinforcedIronPlate, 3), Requirement(ironRod, 6)], assembler, 4))

#------------------------------------------------------------------------------
# Machines - recipes
#------------------------------------------------------------------------------
equipmentWorkshop.addRecipe(Recipe(equipmentWorkshop, 1, 1, [Requirement(ironPlate, 6), Requirement(ironRod, 6)], None, 1))
portableMiner.addRecipe(Recipe(portableMiner, 1, 1, [Requirement(ironPlate, 4), Requirement(wire, 8), Requirement(cable, 4)], equipmentWorkshop, 10))
miner.addRecipe(Recipe(miner, 1, 1, [Requirement(portableMiner, 1), Requirement(ironRod, 5), Requirement(concrete, 1)], None, 1))
smelter.addRecipe(Recipe(smelter, 1, 1, [Requirement(ironRod, 5), Requirement(wire, 8)], None, 1))
constructor.addRecipe(Recipe(constructor, 1, 1, [Requirement(reinforcedIronPlate, 3), Requirement(cable, 2)], None, 1))
assembler.addRecipe(Recipe(assembler, 1, 1, [Requirement(modularFrame, 3), Requirement(rotor, 4), Requirement(cable, 10)], None, 1))

#------------------------------------------------------------------------------
# Requests
#------------------------------------------------------------------------------

def request(craft, quantityPerMin, leaves):
    print('Item choosen : ' + str(quantityPerMin) + ' ' + craft.name + ' per min')
    outputPerMin = 60 / craft.recipes[0].timePerCycle * craft.recipes[0].outputPerCycle
    
    ratio = quantityPerMin / outputPerMin
    for required in craft.recipes[0].listRequirement:
        recursiveRequest(craft.recipes[0].timePerCycle, required, ratio, leaves, 1)
    print('----------------------------------------')
    
def recursiveRequest(craftTimePerCycle, required, ratio, leaves, printLevel):
    outputPerMin = (60 / required.craft.recipes[0].timePerCycle) * required.craft.recipes[0].outputPerCycle
    nbNeededPerMin = required.inputPerCycle * (60 / craftTimePerCycle) * ratio
    nbMachineNeeded = nbNeededPerMin / outputPerMin
    
    print('   ' * printLevel + required.craft.name + ' : ' + str(nbNeededPerMin) + ' (' + str(nbMachineNeeded) + ' ' + required.craft.recipes[0].machine.name + ')')
    
    for subRequired in required.craft.recipes[0].listRequirement:
        if(subRequired.craft.recipes[0] in leaves):
            #print('   ' * printLevel + 'leaf')
            print()
        else:
            recursiveRequest(required.craft.recipes[0].timePerCycle, subRequired, ratio, leaves, printLevel+1)

class Solver:
    def __init__(self, leaves):
        self.leaves = leaves

    def craftToRecipe(self, craft):
        return craft.recipes[0]

    def perMinute(self, craft, bandwidth, depth = 0):
        self.perSecond(craft, bandwidth/60)

    def perSecond(self, craft, bandwidth, depth = 0):
        recipe = self.craftToRecipe(craft)
        operationHz = bandwidth / recipe.outputPerCycle
        nbMachineNeeded = operationHz * recipe.timePerCycle

        print('   ' * depth + craft.name + ' : ' + str(bandwidth*60) + ' (' + str(nbMachineNeeded) + ' ' + recipe.machine.name + ')')

        for subRequired in recipe.listRequirement:
            if(subRequired.craft not in self.leaves):
                self.perSecond(subRequired.craft, operationHz * subRequired.inputPerCycle, depth+1)



def main():
    # By default, the algorithm will continue until the very first elements
    # To stop the tree searching to a certain point, add it in the leaves list
    leaves = [ironOre, copperOre, limestoneOre]
    solver = Solver(leaves)
    solver.perMinute(rotor, 6)
    solver.perMinute(modularFrame, 4)
    solver.perMinute(modularFrame, 8)

    # request(rotor, 6, leaves)
    #
    # request(modularFrame, 4, leaves)
    # request(modularFrame, 8, leaves)

main()