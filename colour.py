from enum import Enum

# Colours
class Colour(Enum):
    RED = 1
    BLUE = 2
    GREEN = 3
    
# Cyclic ordering on colours
    
col_next_map = {
    Colour.RED: Colour.BLUE,
    Colour.BLUE: Colour.GREEN,
    Colour.GREEN: Colour.RED
}

col_prev_map = {
    Colour.RED: Colour.GREEN,
    Colour.BLUE: Colour.RED,
    Colour.GREEN: Colour.BLUE
}
    
def col_next(colour):
    return col_next_map[colour]

def col_prev(colour):
    return col_prev_map[colour]