import json
import random


class RandomCity:
    def __init__(self, file_path):
        self.file_path = file_path
        self.cities = None
        self._limits = None

        if self.file_path:
            self._open_file()

        if self.cities:
            self._get_limits()

    def _open_file(self):
        try:
            with open(self.file_path, "r") as  file_obj:
                json_str = file_obj.read()
                self.cities = json.loads(json_str)
        except Exception as e:
            raise Exception(f"Sorry, {e}")
        
    def _get_limits(self):
        sum_pop = 0
        for city in self.cities:
            sum_pop += city['population']

        if sum_pop:
            limits = []
            rate = 0

            for city in self.cities:
                probability = city['population'] / sum_pop
                rate += probability
                limits.append(
                    {
                        "rate": rate,
                        "name": city['name']
                    }
                )

            self._limits = limits
        else:
            raise Exception("Sorry, there is none person in your cities.")
        
    def get_city(self):
        if self._limits:
            N = random.random()
            for city in self._limits:
                if N < city['rate']:
                    return city['name']
                
            return city['name']
        else:
            raise Exception(f"Sorry, city json file is not correct.")
        