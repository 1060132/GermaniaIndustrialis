import json
housing_count  = 0
farm_count = 0
factory_count = 0


import json

def add_building_to_json(json_file_path, x_coordinate, y_coordinate, building_type):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
        
    if not "counter" in data:
        counts = {
            "Häuser": 0,
            "Fabriken": 0,
            "Farmen": 0
        }
    else:
        counts = data["counter"]

    if building_type == "Fabrik":
        counts["Fabriken"] += 1
    elif building_type == "Haus":
        counts["Häuser"] += 1
    elif building_type == "Farm":
        counts["Farmen"] += 1

    building_index = 1
    while f'Building{building_index}' in data:
        building_index += 1
    new_building_name = f'Building{building_index}'

    new_building = {
        "x-Coordinate": x_coordinate,
        "y-Coordinate": y_coordinate,
        "type": building_type
    }
    
    data[new_building_name] = new_building

    data["counter"] = counts

    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)






add_building_to_json("./first-page.json", 6, 4, "Haus")


import json

def remove_building(json_file_path, x_coordinate, y_coordinate, building_type):
    with open(json_file_path, "r") as file:
        data = json.load(file)

    if not "counter" in data:
        counts = {
            "Häuser": 0,
            "Fabriken": 0,
            "Farmen": 0
        }
    else:
        counts = data["counter"]

    for building_name, building_data in list(data.items()):
        if (building_data["x-Coordinate"] == x_coordinate and
            building_data["y-Coordinate"] == y_coordinate and
            building_data["type"] == building_type):
            if building_type == "Fabrik":
                counts["Fabriken"] -= 1
            elif building_type == "Haus":
                counts["Häuser"] -= 1
            elif building_type == "Farm":
                counts["Farmen"] -= 1
            del data[building_name]

    data["counter"] = counts

    with open(json_file_path, "w") as file:
        json.dump(data, file, indent=4)

