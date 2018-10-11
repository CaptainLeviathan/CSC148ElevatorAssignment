"""CSC148 Assignment 1 - Simulation

=== CSC148 Fall 2018 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This contains the main Simulation class that is actually responsible for
creating and running the simulation. You'll also find the function `sample_run`
here at the bottom of the file, which you can use as a starting point to run
your simulation on a small configuration.

Note that we have provided a fairly comprehensive list of attributes for
Simulation already. You may add your own *private* attributes, but should not
remove any of the existing attributes.
"""
# You may import more things from these modules (e.g., additional types from
# typing), but you may not import from any other modules.
from typing import Dict, List, Any, Optional

import algorithms
# from algorithms import Direction
from entities import Person, Elevator
from visualizer import Visualizer

# TODO: find out if we allowed to have helpers outside of a class
################################################################################
# Helpers
################################################################################


def _dequeue(lst: Any) -> Any:
    """Removes and returns the first item in a list
    """
    item = lst[0]
    lst.remove(item)
    return item


def _elevator_has_room(elevator: Elevator) -> bool:
    """Returns true if the elevator can take more people.
    """
    #Dak - we could also use this:
    #return not elevator._fullness == 1.0
    #thus, if it is full (1.0), then the elevator has no room (returns false)
    return len(elevator.passengers) < elevator.max_capacity


def _average(lst: List[int]) -> Optional[float]:
    """Takes the average of a list of ints
    if the list is empty it will return None
    """

    if len(lst) == 0:
        return None
    total = 0
    for amount in lst:
        total += amount

    return float(total/len(lst))


class Simulation:
    """The main simulation class.

    === Attributes ===
    arrival_generator: the algorithm used to generate new arrivals.
    elevators: a list of the elevators in the simulation
    moving_algorithm: the algorithm used to decide how to move elevators
    num_floors: the number of floors
    visualizer: the Pygame visualizer used to visualize this simulation
    waiting: a dictionary of people waiting for an elevator
             (keys are floor numbers, values are the list of waiting people)
    """
    # TODO Add representaion invariants

    # === Private Attributes ===
    # _total_people: The total number of people who have
    #   arrived during the simulation.
    # _completed_people_times: A list of times for the
    #   people who completed their journey.
    # _number_of_iterations: The number of rounds in the simulation.

    arrival_generator: algorithms.ArrivalGenerator
    elevators: List[Elevator]
    moving_algorithm: algorithms.MovingAlgorithm
    num_floors: int
    visualizer: Visualizer
    waiting: Dict[int, List[Person]]

    _total_people: int
    _completed_people_times: List[int]
    _number_of_iterations: int

    def __init__(self,
                 config: Dict[str, Any]) -> None:
        """Initialize a new simulation using the given configuration."""

        # Initialize the visualizer.
        # Note that this should be called *after* the other attributes
        # have been initialized.

        self.arrival_generator = config['arrival_generator']

        self.elevators = []
        for _ in range(config['num_elevators']):
            self.elevators.append(Elevator(config['elevator_capacity']))

        self.moving_algorithm = config['moving_algorithm']

        self.num_floors = config['num_floors']

        self.waiting = dict()
        for i in range(1, config['num_floors'] + 1):
            self.waiting[i] = []

        self.visualizer = Visualizer(self.elevators,
                                     self.num_floors,
                                     config['visualize'])

        self._total_people = 0
        self._completed_people_times = []
        self._number_of_iterations = 0

    ############################################################################
    # Handle rounds of simulation.
    ############################################################################
    def run(self, num_rounds: int) -> Dict[str, Any]:
        """Run the simulation for the given number of rounds.

        Return a set of statistics for this simulation run, as specified in the
        assignment handout.

        Precondition: num_rounds >= 1.

        Note: each run of the simulation starts from the same initial state
        (no people, all elevators are empty and start at floor 1).
        """
        self._number_of_iterations = num_rounds
        for i in range(num_rounds):
            self.visualizer.render_header(i)

            # Stage 1: generate new arrivals
            self._generate_arrivals(i)

            #Stage 1.5: update people state (Lev added this on)
            self._update_people() #TODO find out if this should come befor or after new arivals

            # Stage 2: leave elevators
            self._handle_leaving()

            # Stage 3: board elevators
            self._handle_boarding()

            # Stage 4: move the elevators using the moving algorithm
            self._move_elevators()

            # Pause for 1 second
            self.visualizer.wait(1)

        return self._calculate_stats()

    def _generate_arrivals(self, round_num: int) -> None:
        """Generate and visualize new arrivals."""
        arrivals = self.arrival_generator.generate(round_num)

        # Takes the people in arrivals and adds them floor by floor to waiting.
        for floor in arrivals.keys():
            self.waiting[floor].extend(arrivals[floor])
            self._total_people += len(arrivals[floor])

        self.visualizer.show_arrivals(arrivals)

    def _update_people(self) -> None:
        """lets people know round has passed"""

        # Updates all the people waiting
        for floor in self.waiting:
            for person in self.waiting[floor]:
                person.round_passed()

        # Updates all the people in the elevators
        for elevator in self.elevators:
            for person in elevator.passengers:
                person.round_passed()

    def _handle_leaving(self) -> None:
        """Handle people leaving elevators."""
        for elevator in self.elevators:
            floor = elevator.floor
            passengers = elevator.passengers
            for passenger in passengers:
                if passenger.target == floor:
                    passengers.remove(passenger)
                    self._completed_people_times.append(passenger.wait_time)
                    self.visualizer.show_disembarking(passenger, elevator)

    def _handle_boarding(self) -> None:
        """Handle boarding of people and visualize."""
        # Looks at each elevator and the floor its on
        # and adds, by order of arrival, the people to the elevators.
        for elevator in self.elevators:
            floor = elevator.floor
            while _elevator_has_room(elevator) and len(self.waiting[floor]) > 0:
                boarder = _dequeue(self.waiting[floor])
                elevator.passengers.append(boarder)
                self.visualizer.show_boarding(boarder, elevator)

    def _move_elevators(self) -> None:
        """Move the elevators in this simulation.

        Use this simulation's moving algorithm to move the elevators.
        """
        directions = self.moving_algorithm.move_elevators(self.elevators,
                                                          self.waiting,
                                                          self.num_floors)
        for elevator, direction in zip(self.elevators, directions):
            elevator.move(direction.value)

        self.visualizer.show_elevator_moves(self.elevators, directions)

    ############################################################################
    # Statistics calculations
    ############################################################################
    def _calculate_stats(self) -> Dict[str, int]:
        """Report the statistics for the current run of this simulation.
        """
        return {
            'num_iterations': self._number_of_iterations,
            'total_people': self._total_people,
            'people_completed': len(self._completed_people_times),
            'max_time': max(self._completed_people_times),
            'min_time': min(self._completed_people_times),
            'avg_time': _average(self._completed_people_times)
        }


def sample_run() -> Dict[str, int]:
    """Run a sample simulation, and return the simulation statistics."""
    config = {
        'num_floors': 6,
        'num_elevators': 6,
        'elevator_capacity': 3,
        'num_people_per_round': 2,
        # Random arrival generator with 6 max floors and 2 arrivals per round.
        'arrival_generator': algorithms.RandomArrivals(6, 2),
        'moving_algorithm': algorithms.RandomAlgorithm(),
        'visualize': True
    }

    sim = Simulation(config)
    stats = sim.run(15)
    return stats


if __name__ == '__main__':
    # Uncomment this line to run our sample simulation (and print the
    # statistics generated by the simulation).
    print(sample_run())

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['entities', 'visualizer', 'algorithms', 'time'],
        'max-nested-blocks': 4
    })
