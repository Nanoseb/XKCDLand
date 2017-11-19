# Resources:
# Money
# Food
# Corners (priesthood) (positive only!)
# Soldiers (positive only!)
available_buildings = {
    "Home": {'Name': "Home",
             'Resource Change': {'food': 2,
                                 'corners': 4},
             'Initial Cost': {},
             'Next': "Castle",
             'Build Key': None,
             'Min Corners': 4},

    "Castle": {'Name': "Castle",
               'Resource Change': {'food': -100,
                                   'money': -100},
               'Initial Cost': {'money': 5000},
               'Min Corners': 10,
               'Build Key': None,
               'Next': None},

    "Market": {'Name': "Market",
               'Resource Change': {'food': -1,
                                   'money': 1},
               'Initial Cost': {'food': 5},
               'Min Corners': 4,
               'Build Key': 'm',
               'Next': "Restaurant"},

    "Restaurant": {'Name': "Restaurant",
                   'Resource Change': {'food': -5,
                                       'money': 3},
                   'Initial Cost': {'food': 30,
                                    'money': 2},
                   'Min Corners': 7,
                   'Build Key': None,
                   'Next': None},

    "Farm": {'Name': "Farm",
             'Resource Change': {'food': 1},
             'Initial Cost': {'money': 2},
             'Min Corners': 4,
             'Build Key': 'f',
             'Next': "Factory"},

    "Factory": {'Name': "Factory",
                'Resource Change': {'food': 5},
                'Initial Cost': {'money': 20},
                'Min Corners': 8,
                'Build Key': None,
                'Next': None},

    "School": {'Name': "School",
               'Resource Change': {'food': -1,
                                   'money': -1,
                                   'corners': 5},
               'Initial Cost': {'money': 5},
               'Min Corners': 4,
               'Build Key': 's',
               'Next': "Church"},

    "Church": {'Name': "Church",
               'Resource Change': {'food': -1,
                                   'money': -1,
                                   'corners': 6},
               'Initial Cost': {'money': 5},
               'Min Corners': 5,
               'Build Key': None,
               'Next': "Hospital"},

    "Hospital": {'Name': "Hospital",
                 'Resource Change': {'food': -1,
                                     'money': -1,
                                     'corners': 8},
                 'Initial Cost': {'money': 5},
                 'Min Corners': 7,
                 'Build Key': None,
                 'Next': "Priesthood"},

    "Priesthood": {'Name': "Priesthood",
                   'Resource Change': {'food': -1,
                                       'money': -1,
                                       'corners': 10},
                   'Initial Cost': {'money': 5},
                   'Min Corners': 8,
                   'Build Key': None,
                   'Next': None},

    "Pontoon": {'Name': "Pontoon",
                'Resource Change': {'food': -1,
                                    'money': -1,
                                    'corners': 7},
                'Initial Cost': {'money': 5},
                'Min Corners': 6,
                'Build Key': 'p',
                'Next': None},

    "Barracks": {'Name': "Barracks",
                 'Resource Change': {'food': -10,
                                     'money': -2,
                                     'corners': 4},
                 'Initial Cost': {'money': 5},
                 'Min Corners': 5,
                 'Build Key': 'b',
                 'Next': None},

}


building_messages = {
    'on_existing_building': "sorry, you might be mighty, but you can't build where there already is stone laid",
    'build_success': "A new building was built",
    'no_resource': "Not sufficient resources!",
    'upgrade_success': "Building was successfully upgraded",
    'not_on_building': "Before upgrading, you have to first build!",
    'no_upgrade_available': "This building is already awesome, no need to make it better?!"}
