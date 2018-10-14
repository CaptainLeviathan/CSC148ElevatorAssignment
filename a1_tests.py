"""CSC148 Assignment 1: Sample tests

=== CSC148 Fall 2018 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains sample tests for Assignment 1.

Warning: This is an extremely incomplete set of tests!
Add your own to practice writing tests and to be confident your code is correct.

For more information on hypothesis (one of the testing libraries we're using),
please see
<https://www.teach.cs.toronto.edu/~csc148h/fall/software/hypothesis.html>.

Note: this file is for support purposes only, and is not part of your
submission.
"""
from algorithms import PushyPassenger, RandomAlgorithm, ShortSighted, \
    RandomArrivals, FileArrivals
from simulation import Simulation


def test_random_arrival_generator_zero() -> None:
    """Test the random arrival generator for two rounds: 0 and 5.

    Note that this test just checks that the range of possible values
    for the random people are correct.
    """
    max_floor = 5
    num_per_round = 2
    random_generator = RandomArrivals(max_floor, num_per_round)

    for round_num in [0, 5]:
        arrivals = random_generator.generate(round_num)
        all_people = []
        for floor, people in arrivals.items():
            # Check that the floor is in the correct range.
            assert 1 <= floor <= max_floor

            all_people.extend(people)

        # Check that the right number of people were generated.
        assert len(all_people) == num_per_round

        for p in all_people:
            # Check floor boundaries
            assert 1 <= p.start <= max_floor
            assert 1 <= p.target <= max_floor

            # Check that the start and target floors are different.
            assert p.start != p.target


def test_file_arrival_generator() -> None:
    """Test the CSV arrival generator for the given sample_arrivals file.
    """
    max_floor = 5
    file_generator = FileArrivals(max_floor, 'sample_arrivals.csv')

    # First try round 0. Note that round numbering starts at 0,
    # but there are no arrivals at round 0 according to the sample file.
    round_zero = file_generator.generate(0)
    for _, people in round_zero.items():
        assert people == []

    # Next try round 1. Two people arrive.
    round_one = file_generator.generate(1)
    for floor, people in round_one.items():
        if floor == 1:
            assert len(people) == 1
            assert people[0].start == 1
            assert people[0].target == 4
        elif floor == 5:
            assert len(people) == 1
            assert people[0].start == 5
            assert people[0].target == 3
        else:
            assert len(people) == 0

    # Next try round 5. One person arrives.
    round_five = file_generator.generate(5)
    for floor, people in round_five.items():
        if floor == 4:
            assert len(people) == 1
            assert people[0].start == 4
            assert people[0].target == 2
        else:
            assert len(people) == 0


def test_random_moving_algorithm() -> None:
    """Test the random moving algorithm.

    Note that while we can't exactly calculate every statistic, we can determine
    whether the statistics have values that are in the right range.

    (And that your simulation runs without crashing.)
    """
    config = {
        'num_floors': 5,
        'num_elevators': 2,
        'elevator_capacity': 1,
        # This is likely not used.
        'num_people_per_round': 2,
        'arrival_generator': FileArrivals(5, 'sample_arrivals.csv'),
        'moving_algorithm': RandomAlgorithm(),
        # Note that we aren't visualizing anything here.
        # Your code should still work properly (and run a lot faster) with this
        # set to False.
        'visualize': False
    }
    sim = Simulation(config)
    num_rounds = 10
    results = sim.run(num_rounds)

    # We can check these statistics exactly.
    assert results['num_iterations'] == num_rounds
    assert results['total_people'] == 4

    # We can check ranges for this one.
    assert 0 <= results['people_completed'] <= results['total_people']

    # We can split up the remaining ones.
    if results['people_completed'] == 0:
        # If no person reached their target floor, report -1 (exact value).
        assert results['max_time'] == -1
        assert results['min_time'] == -1
        assert results['avg_time'] == -1
    else:
        # Check ranges.
        # Note that the minimum number of rounds it should take for someone to
        # reach their target floor is *1*---it's impossible for someone to
        # arrive and reach their target floor in the same round.
        assert (1 <=
                results['min_time'] <=
                results['avg_time'] <=
                results['max_time'] <=
                num_rounds)


def test_pushy_passenger_moving_algorithm() -> None:
    """Test the Pushy Passenger algorithm test with sample_arrivals.csv.

    Note that the configuration is quite a bit more restricted than even
    the sample one given in the starter code. This should make it easier
    to trace out the algorithms by hand.
    """
    config = {
        'num_floors': 5,
        'num_elevators': 2,
        'elevator_capacity': 1,
        # This is likely not used.
        'num_people_per_round': 2,
        'arrival_generator': FileArrivals(5, 'sample_arrivals.csv'),
        'moving_algorithm': PushyPassenger(),
        'visualize': False
    }

    sim = Simulation(config)
    results = sim.run(10)

    assert results['num_iterations'] == 10
    assert results['total_people'] == 4

    # Note: 3 of the 4 people completed their rides.
    # One sad person arrives at round 1 on floor 5, and never reaches their
    # target floor. :(
    assert results['people_completed'] == 3
    assert results['max_time'] == 3
    assert results['min_time'] == 3
    assert results['avg_time'] == 3


def test_short_sighted_moving_algorithm() -> None:
    """Test the Short-Sighted algorithm test with sample_arrivals.csv.

    Note that the configuration is quite a bit more restricted than even
    the sample one given in the starter code. This should make it easier
    to trace out the algorithms by hand.
    """
    config = {
        'num_floors': 5,
        'num_elevators': 2,
        'elevator_capacity': 1,
        # This is likely not used.
        'num_people_per_round': 2,
        'arrival_generator': FileArrivals(5, 'sample_arrivals.csv'),
        'moving_algorithm': ShortSighted(),
        'visualize': False
    }
    sim = Simulation(config)
    results = sim.run(10)

    assert results['num_iterations'] == 10
    assert results['total_people'] == 4

    # Again, three people manage to complete their rides.
    # However, these people are different.
    assert results['people_completed'] == 3
    assert results['max_time'] == 6
    assert results['min_time'] == 3
    assert results['avg_time'] == 4

def test_short_sighted_unit_test():
    config = {
        'num_floors': 4,
        'num_elevators': 2,
        'elevator_capacity': 2,
        # This is likely not used.
        'num_people_per_round': 3,
        'arrival_generator': FileArrivals(5, 'sample_arrivals.csv'),
        'moving_algorithm': ShortSighted(),
        'visualize': False
    }

    sim = Simulation(config)
    results = sim.run(8)

    test_results = {'num_iterations': 8,
                    'total_people': 8,
                    'people_completed': 5,
                    'max_time': 3,
                    'min_time': 2,
                    'avg_time': 2}

    assert test_results == results

def test_pushy_passenger():
    config = {
        'num_floors': 3,
        'num_elevators': 2,
        'elevator_capacity': 2,
        # This is likely not used.
        'num_people_per_round': 3,
        'arrival_generator': FileArrivals(5, 'sample_arrivals.csv'),
        'moving_algorithm': ShortSighted(),
        'visualize': False
    }

    sim = Simulation(config)
    results = sim.run(10)

    test_results = {'num_iterations': 10,
                    'total_people': 13,
                    'people_completed': 12,
                    'max_time': 6,
                    'min_time': 1,
                    'avg_time': 3}

    assert results == test_results

if __name__ == '__main__':
    import pytest
    pytest.main(['a1_tests.py'])
