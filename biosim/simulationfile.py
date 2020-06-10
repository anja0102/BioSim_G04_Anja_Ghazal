from biosim.island import Island
import numpy as np
np.random.seed(1)

listof = [{'species': 'Herbivore', 'age': 0, 'weight': 20} for _ in range(50)]

i = Island()
i.create_new_cell()

for cell in i.cell_list:
    cell.place_animals(listof)

for cell in i.cell_list:
    print(  len(cell.herbivores_list))

num_years = 200

num_animals_everyyear=[]
fitness_of_one_animal = []
for year in range(num_years):
    i.grow_fodder()
    i.feed_animals()
    # for cell in i.cell_list:
    #     # for anim in cell.herbivores_list:
    #     fitness_of_one_animal.append(cell.herbivores_list[0].calculate_fitness())

    i.procreation()
    # for cell in i.cell_list:
    #     # for anim in cell.herbivores_list:
    #     print(cell.herbivores_list[0].calculate_fitness(), end=',')
    # print('\n')
    # for cell in i.cell_list:
    #     print('after proc', len(cell.herbivores_list))
    i.death()
    i.aging()

    for cell in i.cell_list:
        num_animals_everyyear.append(cell.get_num_animals())

print(num_animals_everyyear)
print(fitness_of_one_animal)

# import matplotlib.pyplot as plt
# plt.plot( list( range(len(fitness_of_one_animal))), fitness_of_one_animal,'--' )
# plt.show()

