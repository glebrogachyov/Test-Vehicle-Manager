import json

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


class VehicleManager:
    def __init__(self, url: str, api_route: str = "/vehicles"):
        self._url = url + api_route
        self._vehicles: list[Vehicle] | None = None
        self._params = {"id": int, "name": str, "model": str, "year": int, "color": str, "price": int,
                        "latitude": float, "longitude": float}

    def get_vehicles(self):
        response = requests.get(self._url)
        print("content:", response.content)
        print("status_code:", response.status_code)
        print("headers:", response.headers)
        print("text:", response.text)

    def filter_vehicles(self, params: dict):
        print(params)
        if not set(params.keys()).issubset(self._params):
            return "error. allowed parameters: 'name', 'model', 'year', 'color', 'price', 'latitude', 'longitude'."
        for param in params:
            print(param)

    def get_vehicle(self, vehicle_id: int):
        pass

    def add_vehicle(self, vehicle: Vehicle):
        pass

    def update_vehicle(self, vehicle: Vehicle):
        pass

    def delete_vehicle(self, id: int):
        requests.delete(self._url + f"/{id}")

    def get_distance(self, id1: int, id2: int):
        pass

    def get_nearest_vehicle(self, id: int):
        pass
