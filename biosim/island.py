class BioSim:
    pass


class island:
    """
    - age
    - cells of type "celltype"
    - animals (inside celltype)
    -
    :return:
    """
    def __init__(self):
        self.cell_list=[]  #list to be populated in biosim class

    #def grow_fodder:
    #    for cell in cell_list:
    #        cell.set_fodder()

    def feed_animals(self):
        pass

    def procreation(self):
        pass

    def migration(self):
        pass

    def aging(self):
        pass

    def looseWeight(self):
        pass

    def death(self):
        pass

    #def eating for every cell


class Cell:
    """
    Creating cell structure to describe properties in every square (cell)
    Common for all cells:
     - coordinates
     - egde_cells for migration
     - animals
     - fodder_amount
     -

    :return:
    """
    def __init__(self):
        self.animals=[]
        self.available_fodder=0

    def place_animals(self):
        pass

    def animals_eat(self):  #herbivore feeding
        for animal in self.animals:
            if self.available_fodder >= animal.get_F():
                self.available_fodder -= animal.eat()

    def get_fodder(self):
        return self.available_fodder

class water(Cell):
    def __init__(self):
        self.animals = []
        self.available_fodder = 0

    def set_fodder(self):
        self.available_fodder=0

class desert(Cell):
    def __init__(self):
        self.animals = []
        self.available_fodder = 0

    def set_fodder(self):
        self.available_fodder=0

class highland(Cell):
    def __init__(self):
        self.animals = []
        self.available_fodder = 300

    def set_fodder(self):
        self.available_fodder=300

class Lowland(Cell):
    def __init__(self):
        self.animals = []
        self.available_fodder = 800


    def set_fodder(self):
        self.available_fodder=800
