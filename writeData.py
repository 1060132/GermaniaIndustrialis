import json
import subprocess
housing_count  = 0
farm_count = 0
factory_count = 0
zechen_count = 0

'''
command = ["python3", "-m", "serial.tools.miniterm", "/dev/ttyUSB0", "115200"]
print(command)

subprocess.run(command)

os.system()
ser = serial.Serial(/dev/ttyUSB0, 115200)


While True: 
    readedText = ser.readline()
    print(readedText)
    ser.close()#
    '''





def add_building_to_json(json_file_path, x_coordinate, y_coordinate, building_type):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
        
    if not "counter" in data:
        counts = {
            "Haeuser": 0,
            "Fabriken": 0,
            "Farmen": 0,
            "Zechen": 0
        }
    else:
        counts = data["counter"]
    if building_type == "Fabrik":
        counts["Fabriken"] += 1
    elif building_type == "Haus":
        counts["Haeuser"] += 1
    elif building_type == "Farm":
        counts["Farmen"] += 1
    elif building_type == "Zeche":
        counts["Zechen"] += 1

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





def remove_building(json_file_path, x_coordinate, y_coordinate, building_type):
    with open(json_file_path, "r+") as file:
        data = json.load(file)
        counts = data.get("counter", {"Haeuser": 0, "Fabriken": 0, "Farmen": 0, "Zechen": 0})

        to_remove = []
        for building_name, building_data in data.items():
            if ("x-Coordinate" in building_data and
                "y-Coordinate" in building_data and
                "type" in building_data and
                building_data["x-Coordinate"] == x_coordinate and
                building_data["y-Coordinate"] == y_coordinate and
                building_data["type"] == building_type):
                if building_type == "Fabrik":
                    counts["Fabriken"] -= 1
                elif building_type == "Haus":
                    counts["Haeuser"] -= 1
                elif building_type == "Farm":
                    counts["Farmen"] -= 1
                elif building_type == "Zeche":
                    counts["Zechen"] -= 1
                to_remove.append(building_name)

        for name in to_remove:
            del data[name]

        data["counter"] = counts
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()


add_building_to_json("./first-page.json", 3, 4, "Zeche")
add_building_to_json("./first-page.json", 2, 9, "Zeche")
add_building_to_json("./first-page.json", 3, 7, "Farm")
add_building_to_json("./first-page.json", 2, 5, "Fabrik")
add_building_to_json("./first-page.json", 6, 9, "Haus")