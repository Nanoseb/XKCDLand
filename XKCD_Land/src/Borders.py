import numpy as np



class Border_cell(object):
    def __init__(self, border_id, force_coeficient):
        self.border_id = border_id
        if border_id == 0:
            self.active = False
            self.force = 0
        else:
            self.active = True
            self.force = (256 - border_id) * force_coeficient 


    def attack(self, A_square_soldiers):
        if A_square_soldiers > self.force:
            border_defeated = True
            self.state = False
        else:
            border_defeated = False
            A_square_soldiers = int(A_square_soldiers - self.force/2)

        return A_square_soldiers, border_defeated

        
def desactivate_border(border_id, map_border):
    """
        Desactivate all border that has a particular id
    """
    N, M = np.shape(map_border)
    for i in range(N):
        for j in range(M):
            if map_border[i,j].border_id == border_id:
                map_border[i,j].active = False

    return map_border
        

def is_on_border(position, map_border):
    return map_border[position].active, map_border[position]
