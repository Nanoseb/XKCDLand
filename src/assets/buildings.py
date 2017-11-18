# Resources:
# Money
# Food
# Corners (priesthood) (positive only!)
# Soldiers (positive only!)
from Resources import Building

home = {'Name': "Home",
        'Resource Use': {'food': 1,
                         'corners': 4},
        'Initial Cost': {},
        'Min Corners': 4}

school = {'Name': "School",
          'Resource Use': {'food': -1,
                           'money': -1,
                           'corners': 5},
          'Initial Cost': {'money': 5},
          'Min Corners': 4}

