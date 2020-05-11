import csv
import random


# TODO Randomly generate Suite
# Strip Suite from Street Names
# TODO remove non states
# TODO create city bias weight sum them all up, create a range
class AddressGenerator:
    city_state = []

    def __init__(self):
        self.read_city_state()
        #street_file = open("../testdata/streets.dat")
        street_file = open("testdata/streets.dat")
        self.streets = street_file.readlines()

    def read_city_state(self):
        with open("testdata/city_tx.csv", 'r') as f:
        #with open("../testdata/city_tx.csv", 'r') as f:
            reader = csv.reader(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            i = 0
            for city, state, postal_cd in reader:
                city = city.rstrip()
                state = state.rstrip()
                postal_cd = postal_cd.rstrip()
                self.city_state.append((city, state, postal_cd))
                i += 1

    def get_city(self):
        upper = len(self.city_state) - 1
        ndx = random.randint(0, upper)
        return self.city_state[ndx]

    def get_addr_1(self):
        random_scale = random.randint(2, 5)
        explower = 10 ** random_scale
        expupper = 10 ** (random_scale + 1)
        randm = random.randint(explower, expupper)
        streetndx = random.randint(0, len(self.streets) - 1)
        street_nm = self.streets[streetndx].rstrip()
        addr = str(randm) + " " + street_nm
        return addr

    def get_addr(self):
        line_1 = self.get_addr_1()
        city, state, postal_cd = self.get_city()
        return line_1, city, state, postal_cd


if __name__ == "__main__":
    None
