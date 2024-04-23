import json
import serial
housing_count  = 0
farm_count = 0
factory_count = 0
zechen_count = 0

ser_first = serial.Serial("/dev/ttAMA0", 115200)
ser_second  = serial.Serial("/dev/ttyAMA1", 115200)
ser_third = serial.Serial("dev/ttyAMA2", 115200)






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
            else:
                print("building not to be removed")
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


def convertType(num):





while True:
    data_first = ser_first.read()
    data_left = ser_first.in_waiting()
    data_first += ser_first.read(data_left)
    if not data_first == " ":
        for index, char in enumerate(data_first):
            if char == "x":
                x_coordinate = data_first[index + 1]
                if "," in x_coordinate:
                    break
                else:
                    x_coordinate += data_first[index + 2]
            elif char == "y":
                y_coordinate = data_first[index + 1]
                if "," in y_coordinate:
                    break
                else:
                    y_coordinate += data_first[index + 2]
            elif char == "t":
                type = ""
                while not "." in type:
                    type += data_first[index]
                else:
                    type = type[-1]
    with open("./first-page.json") as file:
    


    data_second = ser_second.read()
    data_left_second = ser_second.in_waiting()
    data_second += ser_second.read(data_left_second)
    if not data_second == " ":
        for index, char in enumerate(data_second):
            if char == "x":
                x_coordinate2 = data_second[index + 1]
                if "," in x_coordinate2:
                    break
                else:
                    x_coordinate2 += data_second[index + 2]
            elif char == "y":
                y_coordinate2 = data_second[index + 1]
                if "," in y_coordinate2:
                    break
                else:
                    y_coordinate2 += data_second[index + 2]
            elif char == "t":
                type2 = ""
                while not "." in type2:
                    type2 += data_second[index]
                else:
                    type2 = type2[-1]

    data_third = ser_third.read()
    data_left_third = ser_third.in_waiting()
    data_third += ser_third.read(data_left_third)
    if not data_third == " ":
        for index, char in enumerate(data_third):
            if char == "x":
                x_coordinate3 = data_third[index + 1]
                if "," in x_coordinate3:
                    break
                else:
                    x_coordinate3 += data_third[index + 2]
            elif char == "y":
                y_coordinate3 = data_third[index + 1]
                if "," in y_coordinate3:
                    break
                else:
                    y_coordinate3 += data_third[index + 2]
            elif char == "t":
                type3 = ""
                while not "." in type3:
                    type3 += data_second[index]
                else:
                    type3 = type3[-1]
            
    



