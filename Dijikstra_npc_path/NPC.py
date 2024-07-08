import math
import random as rand
from time import time


class NpcCharacter:
    def __init__(self, path_finder, init_location, schedule, speed=1):
        self.path_finder = path_finder
        self.schedule = schedule.copy()
        self.working_schedule = schedule.copy()
        
        self.schedule_target_location = self.working_schedule.pop(0)
        self.path = self.path_finder.solve(init_location, self.schedule_target_location)
        self.location = list(self.path.pop(0))
        self.speed = speed
        self.velocity = [0, 0]

        self.current_target_location = self.location

        self.arrival_time = None
        self.delay_time = 0

    def set_path(self, path):
        self.path = path

    def _calc_velocity(self, loc):
        """
        Calculates the 2-dimensional velocities of the NPC based on it's current location and the passed target
        location.
        :param loc: the target location
        :return x and y velocities as a list [x, y]
        """
        d = math.dist(self.location, loc)
        if d == 0:
            return [0, 0]
        x_vel = ((loc[0] - self.location[0])/d) * self.speed
        y_vel = ((loc[1] - self.location[1])/d) * self.speed
        return [x_vel, y_vel]

    def update_target(self, target):
        """

        :param target:
        :return:
        """
        self.current_target_location = target
        self.velocity = self._calc_velocity(target)

    def update_next_schedule_goal(self):
        """

        :return:
        """
        prev = self.schedule_target_location

        # If all locations in the schedule visited, restart the schedule
        if not len(self.working_schedule):
            self.working_schedule = self.schedule.copy()

        self.schedule_target_location = self.working_schedule.pop(0)
        # print(f"Heading to {self.schedule_target_location}")

        self.path = self.path_finder.solve(prev, self.schedule_target_location)

    def move_to_target(self):
        """

        :return:
        """
        self.location[0] += self.velocity[0]
        self.location[1] += self.velocity[1]
        if math.dist(self.location, self.current_target_location) <= self.speed:
            # TODO: Put at target

            # Get next node in the path if there is one
            if len(self.path):
                self.update_target(self.path.pop(0))
                return

            # Schedule goal node is reached
            # Set a delay to sim an activity at the schedule target node
            if self.arrival_time is None:
                self.arrival_time = time()
                self.delay_time = rand.randint(1, 5)
                self.velocity = [0, 0]

            # blocked here from selecting the next scheduled node or resetting the schedule for a set amount of time
            if time() - self.arrival_time < self.delay_time:
                return

            # Update schedule after delay time
            self.arrival_time = None
            self.update_next_schedule_goal()

    def to_string(self):
        """

        :return:
        """
        return f"{self.schedule}\n{self.working_schedule}\n{self.path}"
        
        
if __name__ == "__main__":
    print("Running in test mode")
    import Path_Traversal
    import GameMap

    game_map = GameMap.Map()
    game_map.add_node("A", [0, 0], 1)
    game_map.add_node("B", [0, 1], 0)
    game_map.add_node("C", [0, 2], 1)
    game_map.add_node_connections("A", "B", 1)
    game_map.add_node_connections("B", "C", 1)
    path_finder = Path_Traversal.Dijkstra(game_map)
    p = NpcCharacter(path_finder, "A", ["C"])
    print(p.path)
