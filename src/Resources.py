"""
Handeling resources for xkcd land
Keep track of all buildings and soilders
"""

import assets.buildings

class Building(object):
    def __init__(self, building_specs, position):
        """
        resource_use: dictionary of resources used, pos == output, neg == consumed
        initial cost: dictionary of resources used to build this thing, all pos
        """
        self.Name = building_specs['Name']
        self.InOut = building_specs['Resource Use']
        self.Cost = building_specs['Initial Cost']
        self.MinCorners = building_specs['Min Corners']
        self.Position = position
        self.ActiveState = True   # Buildings are active once they are built
        self.DistanceFromA = 0.

class AllResource(object):
    def __init__(self, start_position):
        self.money = 0
        self.food = 0
        self.fighters = 0
        self.buildings = [Building(assets.buildings.home, start_position)]
