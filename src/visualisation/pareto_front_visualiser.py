# "src/visualisation/pareto_front_visualiser.py"

## The ParetoFrontVisualiser class visualises the Pareto front of a multi-objective optimisation problem.
## It provides visualisation methods for 2D, 3D, parallel coordinates, and radar chart plots.

import matplotlib.pyplot as plt
import numpy as np

class ParetoFrontVisualiser:
    def __init__(self, population, fitness_scores):
        self.population = population
        self.fitness_scores = fitness_scores

    def visualise_2d(self, obj1=0, obj2=1):
        plt.figure(figsize=(10, 8))
        plt.scatter(self.fitness_scores[:, obj1], self.fitness_scores[:, obj2])
        plt.xlabel(f'Objective {obj1 + 1}')
        plt.ylabel(f'Objective {obj2 + 1}')
        plt.title('2D Pareto Front')
        plt.grid(True)
        plt.show()

    def visualise_3d(self, obj1=0, obj2=1, obj3=2):
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(self.fitness_scores[:, obj1], self.fitness_scores[:, obj2], self.fitness_scores[:, obj3])
        ax.set_xlabel(f'Objective {obj1 + 1}')
        ax.set_ylabel(f'Objective {obj2 + 1}')
        ax.set_zlabel(f'Objective {obj3 + 1}')
        ax.set_title('3D Pareto Front')
        plt.show()

    def visualise_parallel_coordinates(self):
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Normalize the data
        normalized_scores = (self.fitness_scores - self.fitness_scores.min(axis=0)) / (self.fitness_scores.max(axis=0) - self.fitness_scores.min(axis=0))
        
        for i in range(len(normalized_scores)):
            ax.plot(range(7), normalized_scores[i], color='blue', alpha=0.1)
        
        ax.set_xticks(range(7))
        ax.set_xticklabels(['Structural', 'Energy', 'Safety', 'Livability', 'Cost', 'Pedestrian Flow', 'Blast Resistance'])
        ax.set_ylabel('Normalized Score')
        ax.set_title('Parallel Coordinates Plot of Pareto Front')
        plt.grid(True)
        plt.show()

    def visualise_radar_chart(self):
        num_vars = 7
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
        
        for i in range(len(self.fitness_scores)):
            values = self.fitness_scores[i].tolist()
            values += values[:1]
            ax.plot(angles, values, linewidth=1, linestyle='solid', alpha=0.1)
            ax.fill(angles, values, alpha=0.1)

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(['Structural', 'Energy', 'Safety', 'Livability', 'Cost', 'Pedestrian Flow', 'Blast Resistance'])
        ax.set_title('Radar Chart of Pareto Front')
        plt.show()


# Example use
if __name__ == "__main__":
    # Generate example data
    population_size = 100
    fitness_scores = np.random.rand(population_size, 7)  # 7 objectives
    
    visualiser = ParetoFrontVisualiser(None, fitness_scores)
    visualiser.visualise_2d()
    visualiser.visualise_3d()
    visualiser.visualise_parallel_coordinates()
    visualiser.visualise_radar_chart()