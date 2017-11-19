

class Border(object):
    def __init__(self, border_specs):
        self.id = border_specs['id']
        self.active = border_specs['active']
        self.soldiers = border_specs['soldiers']
        self.position_px = border_specs['position_px']
        self.sprite = border_specs['sprite']


    def attack(self, A_square_soldiers):
        # update 
        if A_square_soldiers > self.soldiers:
            border_defeated = True
            self.state = False
        else:
            border_defeated = False
            A_square_soldiers = A_square_soldiers - self.soldiers/2


        return A_square_soldiers, border_defeated

        







