from biosim.island import Island

listof = [{'species': 'Herbivore', 'age': 5, 'weight': 25}, {'species': 'Herbivore', 'age': 5, 'weight': 25}
    , {'species': 'Herbivore', 'age': 5, 'weight': 25}, {'species': 'Herbivore', 'age': 5, 'weight': 25}]

i = Island()
i.create_new_cell()

for cell in i.cell_list:
    cell.place_animals(listof)

num_years = 5

for cell in i.cell_list:
    print("number of animals in cell", cell.get_num_animals())

for cell in i.cell_list:
    for animal in cell.herbivores_list:
        print("age : ", animal.get_age())

i.feed_animals()
i.feed_animals()
i.feed_animals()


for year in range(num_years):
    i.feed_animals()
    i.procreation()
    i.aging()
    i.loose_weight()
    i.death()

for cell in i.cell_list:
    print("number of animals in cell", cell.get_num_animals())

for cell in i.cell_list:
    for animal in cell.herbivores_list:
        print("age after aging: ", animal.get_age())