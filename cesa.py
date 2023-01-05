import random
import sys


class Transport():
    transport_methods: list = []

    def __init__(self, name, co2, speed, permeability, min_distance, max_distance, enjoyability):
        self.name = str(name)
        self.co2 = float(co2)
        self.speed = float(speed)
        self.permeability = float(permeability)
        self.min_distance = float(min_distance)
        self.max_distance = float(max_distance)
        self.enjoyability = float(enjoyability)

    def __repr__(self):
        return f'{self.name} : {self.co2} CEQ, {self.speed} km/h, {self.permeability}, ({self.min_distance} - {self.max_distance}) km\n'

    @classmethod
    def get_transport_statistic(cls, distance):
        for transport_method in cls.transport_methods:
            if transport_method.min_distance < distance and transport_method.max_distance > distance:
                return (transport_method.co2*distance, distance/transport_method.speed)
        raise SimulationException("TransportStatisticsException")


class SimulationException(Exception):
    def __init__(self, name):
        super()
        self.name = name


class Person():
    def __init__(self, shop_distance, work_distance, socialize_distance):
        self.shop_distance = shop_distance
        self.work_distance = work_distance
        self.socialize_distance = socialize_distance


def simulate(people: int, time: int, inhomogenousness: float):
    distance_traveled: int = 0
    co2: int = 0
    morale: int = 0
    people: list = [Person(inhomogenousness * random.random(), inhomogenousness * 4 * random.random(),
                           inhomogenousness * 2 * random.random()) for _ in range(people)]
    for week in range(time):
        for person in people:
            work = [
                item * 5/7 for item in Transport.get_transport_statistic(person.work_distance)]
            socialize = [
                item * 3.5/7 for item in Transport.get_transport_statistic(person.socialize_distance)]
            shop = [
                item * 2/7 for item in Transport.get_transport_statistic(person.shop_distance)]
            co2 += work[0] + socialize[0] + shop[0]
    return (distance_traveled, co2, morale)


def main():
    pass


if __name__ == '__main__':
    main()
    results: list[tuple] = []
    transport: list[Transport]
    for design in [[5, 'current'], [2, 'doable'], [1, 'futuristic']]:
        with open(design[1] + '.csv', 'r') as f:
            Transport.transport_methods = [Transport(*line.split(','))
                                           for line in f.read().split('\n') if line[0] != '#']
        print(
            f'when using {design} we can achieve the following statistics over a span of {int(sys.argv[2]) / 55} years with {sys.argv[1]} people:')
        simulation = simulate(int(sys.argv[1]), int(sys.argv[2]), float(design[0]))
        results.append(simulation)
        print("DISTANCE, CO2, MORALE:", *simulation)
    print(f'the co2 savings of the corresponding models are:\n C->F {100 * (1 - results[2][1] / results[0][1])} %\n C->D {100 * (1 - results[1][1] / results[0][1])} %\n D->F {100 * (1 - results[2][1] / results[1][1])} %')
