"""This modual allows you to take direct control of the elevators and make tests
YAY!!"""
from simulation import Simulation
from algorithms import ArrivalGenerator, MovingAlgorithm, Direction

import csv
from typing import Dict, List, Optional

from entities import Person, Elevator

csv_report = []

class ManualArrivalGenerator(ArrivalGenerator):
    """Generate a fixed number of random people each round.

    Generate 0 people if self.num_people is None.

    For our testing purposes, this class *must* have the same initializer header
    as ArrivalGenerator. So if you choose to to override the initializer, make
    sure to keep the header the same!

    Hint: look up the 'sample' function from random.

    === Attributes ===
    max_floor: The maximum floor number for the building.
               Generated people should not have a starting or target floor
               beyond this floor.
    num_people: The number of people to generate, or None if this is left
                up to the algorithm itself.

    === Representation Invariants ===
    max_floor >= 2
    num_people is None or num_people >= 0
    """
    max_floor: int
    num_people: Optional[int]

    def __init__(self, max_floor: int, num_people: Optional[int]) -> None:
        """Initialize a new ArrivalGenerator.

        Preconditions:
            max_floor >= 2
            num_people is None or num_people >= 0
        """
        ArrivalGenerator.__init__(self, max_floor, num_people)

    def generate(self, round_num: int) -> Dict[int, List[Person]]:
        """Return the new arrivals for the simulation at the given round.

        The returned dictionary maps floor number to the people who
        arrived starting at that floor.

        You can choose whether to include floors where no people arrived.
        """

        arivals = dict()
        print(f'=== Round {round_num} ===')
        csv_report.append([round_num])
        for i in range(self.num_people):
            if 'y' == input('make person? (y/n)').lower() :
                start = int(input(f'person {i} start floor: '))
                target = int(input(f'person {i} target floor: '))
                person = Person(start, target)
                csv_report[-1].extend([start, target])
                if start in arivals:
                    arivals[start].append(person)
                else:
                    arivals[start] = [person]
        return arivals


class ManualMovingAlgorithm(MovingAlgorithm):
    """Prompts user on how to move elevators"""
    def move_elevators(self,
                       elevators: List[Elevator],
                       waiting: Dict[int, List[Person]],
                       max_floor: int) -> List[Direction]:
        """Return a list of directions for each elevator to move to.

        As input, this method receives the list of elevators in the simulation,
        a dictionary mapping floor number to a list of people waiting on
        that floor, and the maximum floor number in the simulation.

        Note that each returned direction should be valid:
            - An elevator at Floor 1 cannot move down.
            - An elevator at the top floor cannot move up.
        """
        print("waiting passengers")
        waiting_tuples = list(waiting.items())
        waiting_tuples.sort()
        waiting_tuples.reverse()
        for floor, waitters in waiting_tuples:  # this works! OMG!
            print(f'{floor}: {len(waitters)}')

        output = []
        for i in range(len(elevators)):
            #info for logging
            print(f'Current floor is {elevators[i].floor}')
            print("Target floors:")
            for pas in elevators[i].passengers: print(pas.target)

            str = input(f"Direction for elevator {i}: ")
            str = str.upper()
            if str == 'UP':
                output.append(Direction.UP)
            elif str == 'DOWN':
                output.append(Direction.DOWN)
            elif str == 'STAY':
                output.append(Direction.STAY)
            else:
                print("Needs to be either stay, up, or down")

        return output


if __name__ == '__main__':
    num_floors = int(input("number_floors: "))
    num_evevarots = int(input("number_elevator: "))
    elevator_capasity = int(input('elevator_capasity: '))
    num_people_per_round = int(input("number_people_per_round: "))
    num_rounds = int(input("number rounds: "))

    config = {
        'num_floors': num_floors,
        'num_elevators': num_evevarots,
        'elevator_capacity': elevator_capasity,
        'num_people_per_round': num_people_per_round,
        'arrival_generator': ManualArrivalGenerator(num_floors,
                                                    num_people_per_round),
        'moving_algorithm': ManualMovingAlgorithm(),
        'visualize': True
    }

    sim = Simulation(config)
    stats = sim.run(num_rounds)
    #formating the csv file
    csv_str = ""
    for line in csv_report:
        if len(line) > 1: # just to remove any rounds were no one arived
            csv_str = csv_str + ", ".join(str(i) for i in line) + "\n"
    print("=== config ===")
    print(config)
    print("=== Copy to CSV if you want ===")
    print(csv_str)
    print(stats)

