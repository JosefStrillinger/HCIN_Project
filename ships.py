from enum import Enum

class small_ship:
    def __init__(self, pos, positioning):
        self.length = 2
        self.positioning = positioning
        self.pos = pos
        self.hits = 0
        self.alive = True
        
class medium_ship:
    def __init__(self, pos, positioning):
        self.length = 3
        self.positioning = positioning
        self.pos = pos
        self.hits = 0
        self.alive = True
        
class big_ship:
    def __init__(self, pos, positioning):
        self.length = 4
        self.positioning = positioning
        self.pos = pos
        self.hits = 0
        self.alive = True
        
class huge_ship:
    def __init__(self, pos, positioning):
        self.length = 5
        self.positioning = positioning
        self.pos = pos
        self.hits = 0
        self.alive = True
        


class Positions(Enum):
    vertical = 0
    horizontal = 1