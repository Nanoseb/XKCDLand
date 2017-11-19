"""
Handeling resources for xkcd land
Keep track of all buildings and soilders
"""
import numpy as np

from .assets.buildings import building_messages, available_buildings
from .assets import cheats

SOLDIER_COST = 250

def get_building_keys():
    building_keys = {}
    for house in available_buildings:
        key = available_buildings[house]["Build Key"]
        if key:
            building_keys[key] = available_buildings[house]["Name"]
    return building_keys


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
        self.Frame = building_specs['Frame']

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
        self.Buildings = [Building(available_buildings['Home'], start_position)]

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
                if 'corners' in house.InOut:
                    next_corners = max(next_corners, house.InOut['corners'])
        self.Buildings.sort(key=lambda x: x.DistanceFromA)
        self.ResourceDict['corners'] = next_corners
        print(self.ResourceDict)

    def update_resources(self, current_building):
        """
        calculate resource in- and ouput of buildings,
        pay soldiers and reduce number of soldiers if not all can be paid
        """
        for key in current_building.InOut.keys():
            self.ResourceDict[key] += current_building.InOut[key]

        sufficient_soldier_pay = ((self.ResourceDict['soldiers'] <= self.ResourceDict['money']) &
                                  (self.ResourceDict['soldiers'] <= self.ResourceDict['food']))
        if not sufficient_soldier_pay:
            self.ResourceDict['soldiers'] = min(self.ResourceDict['money'],
                                                self.ResourceDict['food'])
        self.ResourceDict['money'] -= self.ResourceDict['soldiers']
        self.ResourceDict['money'] -= self.ResourceDict['soldiers']


    def check_sufficient_resources(self, specifications):
        sufficient_resources = True
        print(specifications)
        for key in specifications['Initial Cost'].keys():
            sufficient_resources &= (specifications['Initial Cost'][key] <= self.ResourceDict[key])
        sufficient_resources &= (specifications['Min Corners'] <= self.ResourceDict['corners'])

        return sufficient_resources

    def check_for_existing_building(self, position):
        """
        Check if there is an existing building at the current position
        if there is, return the name of the building, otherwise return false
        """
        existing_building = False
        for house in self.Buildings:
            if house.Position == position:
                existing_building = house.Name
        return existing_building

    def add_building(self, position, building_specs):
        """
        checks if a building can be built; if so, a building is added.
        Returns screen message depending on building success
        """
        print("Debug: adding building")
        if self.check_for_existing_building(position) is not False:
            return building_messages['on_existing_building']
        else:
            if (
                self.check_sufficient_resources(building_specs) is True or
                cheats.INFINITE_RESOURCES
            ):
                self.Buildings.append(Building(building_specs, position))
                return building_messages['build_success']
            else:
                return building_messages['no_resource']

    def upgrade_building(self, position):
        """
        checks if there is a building, and if it can be upgraded
        checks if a building can be built; if so, a building is added.
        Returns screen message depending on building success
        """
        print("Debug: upgrading building")
        current_building_name = self.check_for_existing_building(position) 
        if current_building_name is False:
            return building_messages['not_on_building']
        else:
            next_building_name = available_buildings[current_building_name]['Next']
            if not next_building_name:
                return building_messages['no_upgrade_available']
            else:
                next_building = available_buildings[next_building_name]
                if self.check_sufficient_resources(next_building) is True:
                    self.Buildings.append(Building(next_building, position))
                    return building_messages['build_success']
                else:
                    return building_messages['no_resource']

    def add_soldier(self, new_soldier):
        """
        Adds or removes soldiers after checking if there are enough resources or soldiers
        """
        soldier_msg = "Updating soldiers"
        if new_soldier < 0:
            if self.ResourceDict['soldiers'] > 0:
                self.ResourceDict['soldiers'] -= 1
        if new_soldier > 0:
            if self.ResourceDict['money'] > SOLDIER_COST:
                self.ResourceDict['money'] -= SOLDIER_COST
                self.ResourceDict['soldiers'] += 1
            else:
                soldier_msg = "Soldiers training costs " + str(SOLDIER_COST) + " Flatmoney..."
        return soldier_msg

