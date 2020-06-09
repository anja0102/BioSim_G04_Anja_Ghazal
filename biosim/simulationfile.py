from biosim.island import Island

listof = [{'species': 'Herbivore', 'age': 5, 'weight': 25} for _ in range(100)]


i = Island()
i.create_new_cell()

for cell in i.cell_list:
    cell.place_animals(listof)

num_years = 100

num_animals_everyyear=[]

for year in range(num_years):
    i.grow_fodder()
    i.feed_animals()
    i.procreation()
    i.aging()
    i.death()

    for cell in i.cell_list:
        num_animals_everyyear.append(cell.get_num_animals())

print(num_animals_everyyear)

import numpy as np
print(np.mean(num_animals_everyyear))