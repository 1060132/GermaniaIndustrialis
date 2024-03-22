import json

def add_building_to_json(json_file_path, x_coordinate, y_coordinate, building_type):
        with open(json_file_path, 'r') as file:
            data = json.load(file)

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

        with open(json_file_path, 'w') as file:
            json.dump(data, file, indent=4)

        print(f'Neues Gebäude "{new_building_name}" wurde erfolgreich hinzugefügt.')






def remove_building(json_file_path, x_coordinate, y_coordinate, building_type):
        with open(json_file_path, "r") as file:
            data = json.load(file)
        
        for building_name, building_data in list(data.items()):
            if (building_data["x-Coordinate"] == x_coordinate and
                building_data["y-Coordinate"] == y_coordinate and
                building_data["type"] == building_type):
                del data[building_name]

        with open(json_file_path, "w") as file:
            json.dump(data, file, indent=4)

