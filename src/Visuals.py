
def cell_to_px(cell_position, a_position, cell_size, window_size):
    """ 
        Convert a cell position (i,j) in the grid to a pixel position on the screen
        return the (x,y) tuple of the top left corner of the square
        if not on the screen, return (None, None)
        /!\ px coordinates and cell coordinates are inverted
    """
    
    a_px_position = (int(window_size[0]/2 - cell_size/2),
                     int(window_size[1]/2 - cell_size/2))

    cell_px_position = ((cell_position[1] - a_position[1])*cell_size + a_px_position[0],
                        (cell_position[0] - a_position[0])*cell_size + a_px_position[1])
    if cell_px_position[0] < -cell_size or \
       cell_px_position[1] < -cell_size or \
       cell_px_position[0] > window_size[0] or \
       cell_px_position[1] > window_size[1]:
        return (None, None)

    return cell_px_position


