# file for exploring simulation

# create 10 animals
# print animal attributes
# let 5 years pass
# print animal attributes

from biosim.animal import Herbivore

animal_list = []


for i in range(10):
    animal = Herbivore()
    animal_list.append(animal)

for animal in animal_list:
    print("Age: ", animal.get_age(), "weight: ",
          animal.get_weight(), "fitness: ", animal.get_fitness())


for i in range(5):
    for animal in animal_list:
        animal.eat()
        animal.get_older()


for animal in animal_list:
    print("Age: ", animal.get_age(), "weight: ",
          animal.get_weight(), "fitness: ", animal.get_fitness())

