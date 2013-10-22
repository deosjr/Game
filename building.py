

Building_encyclopaedia = {}

def add_building(name, f):
    B = Building(name, f)
    Building_encyclopaedia[name] = B

class Building(object):
    def __init__(self, name, f):
        self.name = name
        self.functions = f

add_building("First settler", [("centerfocus", 0.9)]) 
add_building("House", [("centerfocus", 0.5)]) 