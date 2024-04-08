import simpy
import random


NUM_OF_TRUCKS = 3
NUM_OF_BERTHS = 2
NUM_OF_CRANES = 2
CONTAINERS_PER_VESSEL = 150
CONTAINER_MOVE_TIME = 3  # 3 min
TRUCK_MOVE_TIME = 6  # 6 min
ARRIVAL_RATE = 1 / 300  # 5 hours in min


class ContainerTerminal:
    """
    Represents the terminal entity, managing resources such as berths, cranes, and trucks. 
    It handles the processes of vessel berthing, container unloading, and truck movement.
    """

    def __init__(self, env):
        self.env = env
        self.berths = simpy.Resource(env, capacity=NUM_OF_BERTHS)
        self.trucks = simpy.Resource(env, capacity=NUM_OF_TRUCKS)
        self.cranes = simpy.Resource(env, capacity=NUM_OF_CRANES)
        self.berth_offset = 0
        self.crane_offset = 0

    def log_message(self, message):
        """
            Log message along with env.now
        """
        print(f'{self.env.now}: {message}')

    def berth_vessel(self, vessel):
        """
          Requests for an empty berth and holds 
          it until vessel is discharged
        """
        with self.berths.request() as berth:
            yield berth  # waiting for berth
            berth_id = (self.berth_offset % NUM_OF_BERTHS) + 1
            self.berth_offset += 1

            self.log_message(f'Vessel {vessel} berthed at berth {berth_id}')
            yield self.env.process(self.discharge_vessel(vessel))
            self.log_message(f'Vessel {vessel} unloaded')

        self.log_message(f'Vessel {vessel} left the berth {berth_id}')

    def discharge_vessel(self, vessel):
        """
            Requests for an empty crane and unloads 
            containers while waiting for trucks
        """
        with self.cranes.request() as crane:
            yield crane  # waiting for crane
            crane_id = (self.crane_offset % NUM_OF_CRANES) + 1
            self.crane_offset += 1
            containers_unloaded = 0

            while containers_unloaded < CONTAINERS_PER_VESSEL:
                # Check if any truck is available
                if self.trucks.count < NUM_OF_TRUCKS:
                    containers_unloaded += 1
                    self.log_message(
                        f'Crane {crane_id} unloading container {containers_unloaded} from vessel {vessel}')
                    yield self.env.timeout(CONTAINER_MOVE_TIME)
                    self.env.process(self.move_truck_to_yard(
                        containers_unloaded, vessel))
                else:
                    # Wait until a truck becomes available
                    yield self.env.timeout(1)
                    continue

    def move_truck_to_yard(self, container, vessel):
        """
            Moves the container from terminal to yard
        """
        with self.trucks.request() as truck:
            yield truck
            self.log_message(
                f'Container {container} from vessel {vessel} is on its way to yard')
            yield self.env.timeout(TRUCK_MOVE_TIME)
            self.log_message(
                f'Truck carrying container {container} from vessel {vessel} is back at terminal')


def vessel_generator(env, terminal):
    """
        Generates vessels at random intervals based on an exponential distribution,
        simulating their arrival at the terminal.
    """
    vessel_id = 0
    while True:
        yield env.timeout(int(random.expovariate(ARRIVAL_RATE)))
        vessel_id += 1
        terminal.log_message(
            f'Vessel {vessel_id} has arrived and waiting to berth')
        env.process(terminal.berth_vessel(vessel_id))


def run_simulation():
    """
    Initializes the simulation environment, prompts the user to input the simulation time,
    and runs the simulation until the specified time.
    """
    simulation_time = int(input('Please enter simulation time(in min): '))
    env = simpy.Environment()
    terminal = ContainerTerminal(env)
    env.process(vessel_generator(env, terminal))
    env.run(until=simulation_time)


if __name__ == '__main__':
    run_simulation()
