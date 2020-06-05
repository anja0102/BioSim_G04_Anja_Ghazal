class BioSim:
    pass


class Island:
    """
    - age
    - cells of type "celltype"
    - animals (inside celltype)
    -
    :return:
    """

    def __init__(self):
        self.cell_list = []  # list to be populated in biosim class

    # def grow_fodder:
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

    def loose_weight(self):
        pass

    def death(self):
        pass

    # def eating for every cell


class Cell:
    """
    Creating cell structure to describe properties in every square (cell)
    Common for all cells:
     - coordinates
     - edge_cells for migration
     - animals
     - fodder_amount
     -

    :return:
    """

    def __init__(self):
        self.animals = []
        self.available_fodder = 0

    def place_animals(self):
        pass

    def animals_eat(self):  # herbivore feeding
        for animal in self.animals:
            if self.available_fodder >= animal.get_F():
                self.available_fodder -= animal.eat()

    def procreation(self):
        """
        Checks if there are at least one other animal of the same species in this cell
        and having proper weight for both
        then they will make a new offspring.
        Returns
        -------

        """
        for animal in self.animals:



    def get_fodder(self):
        return self.available_fodder


class Water(Cell):
    def __init__(self):
        self.animals = []
        self.available_fodder = 0

    def set_fodder(self):
        self.available_fodder = 0


class Desert(Cell):
    def __init__(self):
        self.animals = []
        self.available_fodder = 0

    def set_fodder(self):
        self.available_fodder = 0


class Highland(Cell):
    def __init__(self):
        self.animals = []
        self.available_fodder = 300

    def set_fodder(self):
        self.available_fodder = 300


class Lowland(Cell):
    def __init__(self):
        self.animals = []
        self.available_fodder = 800

    def set_fodder(self):
        self.available_fodder = 800
