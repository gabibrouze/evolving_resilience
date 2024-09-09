# "src/simulation_engine/pedestrian_flow.py"

## Implements the `PedestrianFlowSimulation` class with detailed pedestrian flow simulation, which includes:
## - Initialisation of pedestrians
## - Generation of exits
## - Generation of obstacles
## - Calculation of forces
## - Update of velocities
## - Update of positions
## - Calculation of congestion
## - Check if all pedestrians have exited
## - Calculation of evacuation efficiency

import numpy as np

class PedestrianFlowSimulation:
    def __init__(self, genome):
        self.genome = genome
        self.width = genome.genes['building_envelope'].children[1].value
        self.length = genome.genes['building_envelope'].children[2].value
        self.num_floors = round(genome.genes['floor_plans'].children[0].value)
        self.num_pedestrians = 80  # Increase to 200 for high-occupancy scenarios
        self.time_steps = 800  # Increase to 2000 for longer simulation time
        self.desired_speed = 1.4  # m/s, average walking speed
        self.max_force = 5.0  # Maximum force applied to pedestrians
        self.relaxation_time = 0.5  # Time for pedestrians to adjust their velocity
        self.panic_factor = 1.5  # Increased movement speed during emergencies

    def simulate(self):
        total_congestion = 0
        total_evacuation_time = 0
        for floor in range(self.num_floors):
            positions, velocities = self.initialise_pedestrians()
            exit_positions = self.generate_exits()
            obstacles = self.generate_obstacles()
            
            # print(f"Initial positions shape: {positions.shape}")
            # print(f"Exit positions shape: {exit_positions.shape}")
            # print(f"Number of obstacles: {len(obstacles)}")
            
            evacuation_time = 0
            for step in range(self.time_steps):
                forces = self.calculate_forces(positions, velocities, exit_positions, obstacles)
                velocities = self.update_velocities(velocities, forces)
                positions = self.update_positions(positions, velocities, obstacles)
                
                congestion = self.calculate_congestion(positions)
                total_congestion += congestion
                
                if self.all_pedestrians_exited(positions, exit_positions):
                    evacuation_time = step + 1
                    # print(f"  All pedestrians exited at step {evacuation_time}")
                    break
            
            if evacuation_time == 0:
                evacuation_time = self.time_steps
                # print(f"  Not all pedestrians exited within the time limit.")
            
            total_evacuation_time += evacuation_time
            # print(f"Floor {floor + 1} evacuation time: {evacuation_time}")

      
        avg_congestion = total_congestion / (self.num_floors * self.time_steps)
        avg_evacuation_time = total_evacuation_time / self.num_floors

        evacuation_efficiency = self.calculate_evacuation_efficiency(avg_evacuation_time)
         
        return {
            "average_congestion": avg_congestion,
            "average_evacuation_time": avg_evacuation_time,
            "evacuation_efficiency": evacuation_efficiency
        }

    def initialise_pedestrians(self):
        positions = np.random.rand(self.num_pedestrians, 2) * [self.width, self.length]
        velocities = np.zeros((self.num_pedestrians, 2))
        # print(f"Initialised {self.num_pedestrians} pedestrians")
        return positions, velocities

    def generate_exits(self):
        num_exits = max(2, int(np.sqrt(self.width * self.length) / 8))
        exits = np.random.rand(num_exits, 2) * [self.width, self.length]
        # print(f"Generated {num_exits} exits at positions:")
        # for i, exit_pos in enumerate(exits):
            # print(f"  Exit {i+1}: ({exit_pos[0]:.2f}, {exit_pos[1]:.2f})")
        return exits

    def generate_obstacles(self):
        num_obstacles = int(np.sqrt(self.width * self.length) / 5)
        obstacles = np.random.rand(num_obstacles, 2) * [self.width, self.length]
        return obstacles

    def calculate_forces(self, positions, velocities, exit_positions, obstacles):
        forces = np.zeros_like(positions)
        
        # Desired force towards nearest exit
        distances_to_exits = np.linalg.norm(positions[:, np.newaxis] - exit_positions, axis=2)
        nearest_exit_indices = np.argmin(distances_to_exits, axis=1)
        desired_directions = exit_positions[nearest_exit_indices] - positions
        norms = np.linalg.norm(desired_directions, axis=1)
        norms[norms == 0] = 1e-6
        desired_directions /= norms[:, np.newaxis]
        desired_velocities = desired_directions * self.desired_speed * self.panic_factor
        forces += (desired_velocities - velocities) / self.relaxation_time

        # Repulsive force from other pedestrians (vectorized)
        diff = positions[:, np.newaxis] - positions
        dist = np.linalg.norm(diff, axis=2)
        np.fill_diagonal(dist, 1e-6)  # Avoid self-interaction
        repulsive_force = np.exp(-dist/0.3)[:, :, np.newaxis] * diff / dist[:, :, np.newaxis]
        forces -= repulsive_force.sum(axis=1)

        # Repulsive force from obstacles
        obstacle_diff = positions[:, np.newaxis] - obstacles
        obstacle_dist = np.linalg.norm(obstacle_diff, axis=2)
        obstacle_dist[obstacle_dist == 0] = 1e-6
        obstacle_force = np.exp(-obstacle_dist/0.5)[:, :, np.newaxis] * obstacle_diff / obstacle_dist[:, :, np.newaxis]
        forces -= obstacle_force.sum(axis=1)

        # Limit max force
        force_magnitudes = np.linalg.norm(forces, axis=1)
        excessive_forces = force_magnitudes > self.max_force
        forces[excessive_forces] *= self.max_force / force_magnitudes[excessive_forces, np.newaxis]

        return forces

    def update_velocities(self, velocities, forces):
        return velocities + forces * self.relaxation_time

    def update_positions(self, positions, velocities, obstacles):
        new_positions = positions + velocities * self.relaxation_time
        # Ensure pedestrians stay within the building and don't overlap with obstacles
        new_positions = np.clip(new_positions, [0, 0], [self.width, self.length])
        for obstacle in obstacles:
            dist_to_obstacle = np.linalg.norm(new_positions - obstacle, axis=1)
            too_close = dist_to_obstacle < 0.5
            new_positions[too_close] = positions[too_close]
        return new_positions

    def calculate_congestion(self, positions):
        distances = np.linalg.norm(positions[:, np.newaxis] - positions, axis=2)
        close_pedestrians = (distances < 0.5).sum() - self.num_pedestrians  # Reduced distance threshold
        return close_pedestrians / self.num_pedestrians

    def all_pedestrians_exited(self, positions, exit_positions):
        distances_to_exits = np.linalg.norm(positions[:, np.newaxis] - exit_positions, axis=2)
        min_distances = np.min(distances_to_exits, axis=1)
        exit_threshold = 1.0  # Increased from 0.5 to 1.0 meter
        all_exited = np.all(min_distances < exit_threshold)
        return all_exited

    def calculate_evacuation_efficiency(self, avg_evacuation_time):
        ideal_time = np.sqrt(self.width**2 + self.length**2) / self.desired_speed
        if avg_evacuation_time == 0:
            return 1.0  # Perfect efficiency if evacuation is instantaneous
        # Cap efficiency at 1.0 to avoid negative values
        return min(1.0, ideal_time / avg_evacuation_time)

# Example use case
if __name__ == "__main__":
    from ..genetic_algorithm.encoding import BuildingGenome
    
    genome = BuildingGenome()
    pedestrian_flow = PedestrianFlowSimulation(genome)
    results = pedestrian_flow.simulate()
    print(results)