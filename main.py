from vehicle_manager import Vehicle, VehicleManager


manager = VehicleManager(url="https://test.tspb.su/test-task")

# Получение списка всех автомобилей
manager.get_vehicles()
# [<Vehicle: Toyota Camry 2021 red 21000>, ...]

# Получение списка автомобилей, у которых поле name равно 'Toyota'
tmp = manager.filter_vehicles(params={"name": "Toyota"})
# [<Vehicle: Toyota Camry 2021 red 21000>]

# Получение автомобиля с id=1
manager.get_vehicle(vehicle_id=1)
# <Vehicle: Toyota Camry 2021 red 21000>
# Добавление нового автомобиля в базу данных

manager.add_vehicle(
    vehicle=Vehicle(
        name='Toyota',
        model='Camry',
        year=2021,
        color='red',
        price=21000,
        latitude=55.753215,
        longitude=37.620393
    )
)

# <Vehicle: Toyota Camry 2021 red 21000>
# Изменение информации об автомобиле с id=1

manager.update_vehicle(
    vehicle=Vehicle(
        id=1,
        name='Toyota',
        model='Camry',
        year=2021,
        color='red',
        price=21000,
        latitude=55.753215,
        longitude=37.620393
    )
)

# <Vehicle: Toyota Camry 2021 red 21000>
# Удаление автомобиля с id=1
manager.delete_vehicle(id=1)

# Расчет расстояния между автомобилями с id=1 и id=2
manager.get_distance(id1=1, id2=2)
# 638005.0864183258

# Нахождение ближайшего автомобиля к автомобилю с id=1
manager.get_nearest_vehicle(id=1)
# <Vehicle Kia Sorento 2019 30000>
