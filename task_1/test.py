from cities import RandomCity

cities = RandomCity('input.json')

result = {}

for city in cities.cities:
    result.setdefault(city['name'], 0)

for N in range(0, 10000):
    city = cities.get_city()
    result[city] += 1

print(result)
