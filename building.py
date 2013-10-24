
Building_encyclopaedia = {}
Sociability = {}

def add_building(name, f):
    B = Building(name, f)
    Building_encyclopaedia[name] = B

def add_sociability(beta1, beta2, lmin, l0, lmax):
    Sociability[(min(beta1, beta2), max(beta1, beta2))] = (lmin, l0, lmax)

class Building(object):
    def __init__(self, name, f):
        self.name = name
        self.functions = f

add_building("First settler", [("centerfocus", 0.9)]) 
add_building("House", [("centerfocus", 0.5), ("sociability", 0.6)]) 

add_sociability("House", "First settler", 10, 30, 200)
add_sociability("House", "House", 10, 30, 50)