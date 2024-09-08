# "src/visualisation/pareto_front_visualiser.py"

## The ParetoFrontVisualiser class visualises the Pareto front of a multi-objective optimisation problem.
## It provides visualisation methods for 2D, 3D, parallel coordinates, and radar chart plots.
import matplotlib.pyplot as plt
import numpy as np

class ParetoFrontVisualiser:
    def __init__(self, population, fitness_scores):
        self.population = population
        self.fitness_scores = np.array(fitness_scores)

    def visualise_2d(self, ax, obj1=0, obj2=1):
        if self.fitness_scores.shape[1] < 2:
            ax.text(0.5, 0.5, 'Not enough data for 2D Pareto front', 
                    horizontalalignment='center', verticalalignment='center')
            ax.set_title('2D Pareto Front (Insufficient Data)')
        else:
            ax.scatter(self.fitness_scores[:, obj1], self.fitness_scores[:, obj2])
            ax.set_xlabel(f'Objective {obj1 + 1}')
            ax.set_ylabel(f'Objective {obj2 + 1}')
            ax.set_title('2D Pareto Front')
            ax.grid(True)

    def visualise_3d(self, ax, obj1=0, obj2=1, obj3=2):
        if self.fitness_scores.shape[1] < 3:
            ax.text(0.5, 0.5, 0.5, 'Not enough data for 3D Pareto front', 
                    horizontalalignment='center', verticalalignment='center')
            ax.set_title('3D Pareto Front (Insufficient Data)')
        else:
            ax.scatter(self.fitness_scores[:, obj1], self.fitness_scores[:, obj2], self.fitness_scores[:, obj3])
            ax.set_xlabel(f'Objective {obj1 + 1}')
            ax.set_ylabel(f'Objective {obj2 + 1}')
            ax.set_zlabel(f'Objective {obj3 + 1}')
            ax.set_title('3D Pareto Front')

    def visualise_parallel_coordinates(self, ax):
        if self.fitness_scores.shape[1] < 2:
            ax.text(0.5, 0.5, 'Not enough data for parallel coordinates plot', 
                    horizontalalignment='center', verticalalignment='center')
            ax.set_title('Parallel Coordinates Plot (Insufficient Data)')
        else:
            # Normalize the data
            normalized_scores = (self.fitness_scores - self.fitness_scores.min(axis=0)) / (self.fitness_scores.max(axis=0) - self.fitness_scores.min(axis=0))
            
            for i in range(len(normalized_scores)):
                ax.plot(range(normalized_scores.shape[1]), normalized_scores[i], color='blue', alpha=0.1)
            
            ax.set_xticks(range(normalized_scores.shape[1]))
            ax.set_xticklabels(['Obj ' + str(i+1) for i in range(normalized_scores.shape[1])])
            ax.set_ylabel('Normalized Score')
            ax.set_title('Parallel Coordinates Plot of Pareto Front')
            ax.grid(True)

    def visualise_radar_chart(self, ax):
        if self.fitness_scores.shape[1] < 3:
            ax.text(0, 0, 'Not enough data for radar chart', 
                    horizontalalignment='center', verticalalignment='center')
            ax.set_title('Radar Chart (Insufficient Data)')
        else:
            num_vars = self.fitness_scores.shape[1]
            angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
            
            # Close the polygon by appending the start point to the end.
            values = self.fitness_scores.mean(axis=0).tolist()
            values += values[:1]
            angles += angles[:1]

            ax.plot(angles, values)
            ax.fill(angles, values, alpha=0.1)
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(['Obj ' + str(i+1) for i in range(num_vars)])
            ax.set_title('Radar Chart of Pareto Front')

# Example use
if __name__ == "__main__":
    # Generate example data
    population_size = 100
    fitness_scores = np.random.rand(population_size, 7)  # 7 objectives
    
    visualiser = ParetoFrontVisualiser(None, fitness_scores)
    
    fig = plt.figure(figsize=(15, 15))
    
    ax1 = fig.add_subplot(221)
    ax2 = fig.add_subplot(222, projection='3d')
    ax3 = fig.add_subplot(223)
    ax4 = fig.add_subplot(224, projection='polar')
    
    visualiser.visualise_2d(ax1)
    visualiser.visualise_3d(ax2)
    visualiser.visualise_parallel_coordinates(ax3)
    visualiser.visualise_radar_chart(ax4)
    
    plt.tight_layout()
    plt.show()