from biosim.cell import Cell, Lowland


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

    def create_new_cell(self):
        c = Lowland()  #Later replaced by function creating different types of land
        self.cell_list.append(c)

    def grow_fodder(self):
        for cell in self.cell_list:
            cell.set_fodder()

    def feed_animals(self):
        for cell in self.cell_list:
            cell.animals_eat()

    def procreation(self):
        for cell in self.cell_list:
            cell.procreation()

    def aging(self):
        for cell in self.cell_list:
            cell.animals_age_by_one_year()

    def death(self):
        for cell in self.cell_list:
            cell.animals_die()

    #def loose_weight(self):
        #Every year, the weight of the animal decreases by eta * omega.
    #    for cell in self.cell_list:
    #        cell.animals_update_weight_annual()

    def migration(self):
        pass


    # def eating for every cell



if __name__ == "__main__":


    i = Island()
    i.create_new_cell()

    for cell in i.cell_list:
        cell.place_animals()
        cell.place_animals()

    for cell in i.cell_list:
        print("fodder:", cell.get_fodder())
        for animal in cell.animal_list:
            print("weight:", animal.get_weight())

    for _ in range(20):
        i.feed_animals()

    for cell in i.cell_list:
        print("fodder:", cell.get_fodder())
        for animal in cell.animal_list:
            print("weight after eating:", animal.get_weight())

    for cell in i.cell_list:
        print("number of animals in cell", cell.get_num_animals())

    i.procreation()

    for cell in i.cell_list:
        print("number of animals after procreation", cell.get_num_animals())

    for cell in i.cell_list:
        for animal in cell.animal_list:
            print("age: ", animal.get_age())

    i.aging()

    for cell in i.cell_list:
        for animal in cell.animal_list:
            print("age after aging: ", animal.get_age())

    for cell in i.cell_list:
        for animal in cell.animal_list:
            print("weight: ", animal.get_weight())

    i.loose_weight()

    for cell in i.cell_list:
        for animal in cell.animal_list:
            print("weight after loosing: ", animal.get_weight())


    for cell in i.cell_list:
        print("number of animals in cell", cell.get_num_animals())
    i.death()
    for cell in i.cell_list:
        print("number of animals after killing", cell.get_num_animals())
