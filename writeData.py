import json
from serial import Serial
import serial
import threading

housing_count = 0
farm_count = 0
factory_count = 0
zechen_count = 0

ser_first = serial.Serial("/dev/ttAMA0", 115200)
ser_second = serial.Serial("/dev/ttyAMA1", 115200)
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

def checker_json(type, x_coordinate, y_coordinate):
            with open("./first-page-checker.json", 'r') as file:
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
            if type == "Fabrik":
                counts["Fabriken"] += 1
            elif type == "Haus":
                counts["Haeuser"] += 1
            elif type == "Farm":
                counts["Farmen"] += 1
            elif type == "Zeche":
                counts["Zechen"] += 1

            building_index = 1
            while f'Building{building_index}' in data:
                building_index += 1
            new_building_name = f'Building{building_index}'

            new_building = {
                "x-Coordinate": x_coordinate,
                "y-Coordinate": y_coordinate,
                "type": type
            }
            
            data[new_building_name] = new_building

            data["counter"] = counts

            with open("./first-page-checker.json", 'w') as file:
                json.dump(data, file, indent=4)


def convertType(num):
    if num == 1:
        modell =  "Haus"
    elif num == 2:
        modell = "Farm"
    elif num == 3:
        modell = "Fabrik"
    elif num == 4:
        modell = "Zeche"
    return modell

def read_serial_data(ser):
    while True:
        data = ser.read()
        data_left = ser.in_waiting()
        data += ser.read(data_left)
        if not data == " ":
            for index, char in enumerate(data):
                if char == "x":
                    x_coordinate = data[index + 1]
                    if "," in x_coordinate:
                        break
                    else:
                        x_coordinate += data[index + 2]
                elif char == "y":
                    y_coordinate = data[index + 1]
                    if "," in y_coordinate:
                        break
                    else:
                        y_coordinate += data[index + 2]
                elif char == "t":
                    building_type = ""
                    while not "." in building_type:
                        building_type += data[index]
                    else:
                        building_type = building_type[-1]
            building_type = convertType(building_type)

            thread_add = threading.Thread(target=add_building_to_json, args=("./first-page.json", x_coordinate, y_coordinate, building_type))
            thread_checker = threading.Thread(target=checker_json, args=(building_type, x_coordinate, y_coordinate))

            thread_add.start()
            thread_checker.start()

            thread_add.join()
            thread_checker.join()

thread_first = threading.Thread(target=read_serial_data, args=(ser_first,))
thread_second = threading.Thread(target=read_serial_data, args=(ser_second,))
thread_third = threading.Thread(target=read_serial_data, args=(ser_third,))

thread_first.start()
thread_second.start()
thread_third.start()

thread_first.join()
thread_second.join()
thread_third.join()