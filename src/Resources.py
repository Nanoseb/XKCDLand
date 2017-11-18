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

    def check_activity(self, available):
        # bear in mind: consumed good are negative in InOut
        state = True
        for key in self.InOut.keys():
            state = state & (available[key] + self.InOut[key] >= 0)
        state = state & (available['corners'] >= self.MinCorners)
        self.ActiveState = state
        
class AllResource(object):
    def __init__(self, start_position):
        self.ResourceDict = {'money': 0,
                             'food': 0,
                             'corners': 4,
                             'soldiers': 0}
        self.Buildings = [Building(assets.buildings.home, start_position)]

    def calculate_next(self, current_position):
        """
        manages all resources for the next time step
        """
        next_corners = 4  # 4 is the minimum number of corners

        for house in self.Buildings:
            house.update_distance_from_a(current_position)
            house.check_activity(self.ResourceDict)
            if house.ActiveState is True:
                self.update_resources(house)
                next_corners = max(next_corners, house.InOut['corners'])
        self.Buildings.sort(key=lambda x: x.DistanceFromA) 
        self.ResourceDict['corners'] = next_corners
        print(self.ResourceDict)

    def update_resources(self, current_building):
        for key in current_building.InOut.keys():
            self.ResourceDict[key] += current_building.InOut[key]

    def check_sufficient_resources(self, specifications):
        # TODO: implement actual check
        return True

    def check_for_existing_building(self, position):
        # TODO: implement actual check
        return True

    def add_building(self, building_specs, position):
        """
        checks if a building can be built; if so, a building is added.
        Returns screen message depending on building success
        """
        if self.check_for_existing_building(position) is True:
            return assets.buildings.messages['on_existing_building']
        else:
            if self.check_sufficient_resources(building_specs) is True:
                self.Buildings.append(Building(building_specs, position))
                return assets.buildings.messages['success']
            else:
                return assets.buildings.messages['no_resource']
