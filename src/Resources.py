"""
Handeling resources for xkcd land
Keep track of all buildings and soilders
"""
import numpy as np
import assets.buildings

class Building(object):
    def __init__(self, building_specs, position):
        """
        resource_use: dictionary of resources used, pos == output, neg == consumed
        initial cost: dictionary of resources used to build this thing, all pos
        """
        self.Name = building_specs['Name']
        self.InOut = building_specs['Resource Change']
        self.Cost = building_specs['Initial Cost']
        self.MinCorners = building_specs['Min Corners']
        self.Position = position
        self.ActiveState = True   # Buildings are active once they are built
        self.DistanceFromA = 0.

    def update_distance_from_a(self, a_position):
        self.DistanceFromA = np.sqrt((self.Position[0] - a_position[0])**2 +
                                     (self.Position[1] - a_position[1])**2)

    def check_activity(self, avail_money, avail_food, current_corners):
        # bear in mind: consumed good are negative in InOut
        self.ActiveState = ((avail_money + self.InOut['money'] >= 0) &
                            (avail_food + self.InOut['food'] >= 0) &
                            (current_corners >= self.MinCorners))
        
class AllResource(object):
    def __init__(self, start_position):
        self.Money = 0
        self.Food = 0
        self.Corners = 4
        self.Soldiers = 0
        self.Buildings = [Building(assets.buildings.home, start_position)]

    def calculate_next(self, current_position):
        """
        manages all resources for the next time step
        """
        next_corners = 4  # 4 is the minimum number of corners

        for house in self.Buildings:
            house.update_distance_from_a(current_position)
            house.check_activity(self.Money, self.Food, self.Corners)
            if house.ActiveState is True:
                self.update_resources(house)
                next_corners = max(next_corners, house.InOut['corners'])
        self.Buildings.sort(key=lambda x: x.DistanceFromA) 
        self.Corners = next_corners
        print("calculating next resources")
        print(self.Food)

    def update_resources(self, current_building):
        self.Money += current_building.InOut['money']
        self.Food += current_building.InOut['food']
        self.Soldiers += current_building.InOut['soldiers']
