# file for exploring simulation

# create 10 animals
# print animal attributes
# let 5 years pass
# print animal attributes

from biosim.animal import Animal

animal_list = []


for i in range(10):
    animal = Animal()
    animal_list.append(animal)

for animal in animal_list:
    print("Age: ", animal.get_age(), "weight: ",
          animal.get_weight(), "fitness: ", animal.get_fitness())


for i in range(50):
    for animal in animal_list:
        animal.eat()
        animal.grow_older()


from biosim.island import Cell, Lowland

c = Lowland()
c.animals = animal_list


print("fodder: ", c.get_fodder())
c.animals_eat()
print("fodder: ", c.get_fodder())

