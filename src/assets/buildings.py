# Resources:
# Money
# Food
# Corners (priesthood) (positive only!)
# Soldiers (positive only!)

home = {'Name': "Home",
        'Resource Change': {'food': 1,
                            'corners': 4},
        'Initial Cost': {},
        'Min Corners': 4}

school = {'Name': "School",
          'Resource Change': {'food': -1,
                              'money': -1,
                              'corners': 5},
          'Initial Cost': {'money': 5},
          'Min Corners': 4}


messages = {'on_existing_building': "sorry, you might be mighty, but you can't build where there already is stone laid",
            'build_success': "A new building was built",
            'no_resource': "Not sufficient resources!",
            'upgrade_success': "Building was successfully upgraded",
            'not_on_building': "Before upgrading, you have to first build!"
            }
