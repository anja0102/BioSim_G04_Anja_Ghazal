

from biosim.animal import Herbivore

animal_list = []


for i in range(5):
    animal = Herbivore()
    animal_list.append(animal)


from biosim.island import Cell, Lowland

c = Lowland()
c.animals = animal_list

print("fodder: ", c.get_fodder())
c.animals_eat()
print("fodder: ", c.get_fodder())

