from biosim.island import Island

listof = [{'species': 'Herbivore', 'age': 5, 'weight': 25}, {'species': 'Herbivore', 'age': 5, 'weight': 25}
    , {'species': 'Herbivore', 'age': 5, 'weight': 25}, {'species': 'Herbivore', 'age': 5, 'weight': 25}]

i = Island()
i.create_new_cell()

for cell in i.cell_list:
    cell.place_animals(listof)

num_years = 200

num_animals_everyyear=[]

for year in range(num_years):
    i.grow_fodder()
    i.feed_animals()
    i.procreation()
    i.aging()
    i.loose_weight()
    i.death()

    for cell in i.cell_list:
        num_animals_everyyear.append(cell.get_num_animals())

print(num_animals_everyyear)