import math
from math import cos, sin, acos

import requests


class Vehicle:
    def __init__(self, name: str, model: str, year: int, color: str, price: int, latitude: float,
                 longitude: float, id: int = None):
        self.id = id
        self.name = name
        self.model = model
        self.year = year
        self.color = color
        self.price = price
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return f"<Vehicle: {self.name} {self.model} {self.year} {self.color} {self.price}>"

    def to_json(self, with_id=False):
        id_field = f'"id":{self.id},' if with_id else ''
        return f'{{{id_field}"name":{self.name},"model":{self.model},"year":{self.year},"color":{self.color},' \
               f'"price":{self.price},"latitude":{self.latitude},"longitude":{self.longitude}}}'


class VehicleManager:
    def __init__(self, url: str, api_route: str = "/vehicles"):
        self._url = url + api_route
        self._vehicles: list[Vehicle] | None = None  # для кэширования результата последнего запроса
        self._params = {"id": int, "name": str, "model": str, "year": int, "color": str, "price": int,
                        "latitude": float, "longitude": float}

    def get_vehicles(self) -> list[Vehicle]:
        response = requests.get(self._url)
        self._vehicles = self.json_load_list_items(self.json_split_list(response.text))
        return self._vehicles

    def filter_vehicles(self, params: dict) -> list[Vehicle]:
        vehicles = self.get_vehicles()
        if not set(params.keys()).issubset(self._params):
            raise KeyError("error. allowed fields: 'name', 'model', 'year', 'color', 'price', 'latitude', 'longitude'")
        for key, val in params.items():
            vehicles = [veh for veh in vehicles if getattr(veh, key) == val]
        return vehicles

    def get_vehicle(self, vehicle_id: int) -> Vehicle:
        response = requests.get(self._url + f"/{vehicle_id}")
        vehicle = self.json_load_one_item(response.text.strip('"'))
        return vehicle

    def add_vehicle(self, vehicle: Vehicle) -> Vehicle:
        requests.post(self._url, data=vehicle.to_json())
        return vehicle

    def update_vehicle(self, vehicle: Vehicle) -> Vehicle:
        requests.put(self._url, data=vehicle.to_json(with_id=True))
        return vehicle

    def delete_vehicle(self, id: int):
        requests.delete(self._url + f"/{id}")
        return None

    def get_distance(self, id1: int, id2: int, use_cached=False) -> float:
        if not use_cached:
            vehicle_one = self.get_vehicle(id1)
            vehicle_two = self.get_vehicle(id2)
        else:
            vehicle_one = self._vehicles[id1 - 1]
            vehicle_two = self._vehicles[id2 - 1]

        lat1 = math.radians(vehicle_one.latitude)
        lat2 = math.radians(vehicle_two.latitude)
        lon1 = math.radians(vehicle_one.longitude)
        lon2 = math.radians(vehicle_two.longitude)

        dst = acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon2 - lon1)) * 6371 * 10**3

        return dst

    def get_nearest_vehicle(self, id: int) -> Vehicle:
        vehicles = self.get_vehicles()
        vehicles_distance = [self.get_distance(id, to_cmp, use_cached=True) for to_cmp in range(1, len(vehicles) + 1)]
        res = [x for _, x in sorted(zip(vehicles_distance, vehicles), key=lambda pair: pair[0])]
        return res[1]

    @staticmethod
    def json_split_list(json_str: str) -> list[str]:
        """ Возвращает список json-строк, каждая из которых описывает объекта класса Vehicle """
        json_str = json_str.strip()
        if not json_str.startswith("[{") and json_str.startswith("}]"):
            raise KeyError("error. wrong json list")
        return json_str[2:-2].replace(", ", ",").split("},{")

    def json_load_list_items(self, items_list: list[str]) -> list[Vehicle]:
        """ Принимает на вход список json-строк, возвращает список десериализованных объектов класса Vehicle """
        result = []
        for item in items_list:
            result.append(self.json_load_one_item(item))
        return result

    def json_load_one_item(self, k_v_pairs: str) -> Vehicle:
        """ Принимает json-строку, возвращает объект класса Vehicle """
        tmp_item = {}
        pairs = k_v_pairs[1:-1].split(",")
        for idx, pair in enumerate(pairs):
            key, value = pair.split(":")
            key = key.strip('"')
            if type_ := self._params.get(key):
                if type_ == str:
                    value = value.strip('"')
                tmp_item[key] = type_(value)
            else:
                raise KeyError("error. wrong fields in json.")
        return Vehicle(**tmp_item)
