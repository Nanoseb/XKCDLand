# Resources:
# Money
# Food
# Corners (priesthood) (positive only!)
# Soldiers (positive only!)


home = Building("Home", 
                {"food": 1,
                 "corners": 4},
                 {})

class Building(object):
    def __init__(self, name, resource_use, initial_cost):
        """
        resource_use: dictionary of resources used, pos == output, neg == consumed
        initial cost: dictionary of resources used to build this thing, all pos
        """
        self.Name = name
        self.InOut = resource_use
        self.Cost = initial_cost
