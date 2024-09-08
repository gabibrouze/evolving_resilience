# "src/genetic_algorithm/evolution.py"

## Implements the `EvolutionaryAlgorithm` class, including methods for:
## - Evaluating fitness
## - Tournament selection
## - Evolving the population

import traceback

import numpy as np
from .encoding import BuildingGenome
from ..simulation_engine.structural_integrity import StructuralIntegrity
from ..simulation_engine.energy_simulation import EnergySimulation
from ..simulation_engine.safety_assessment import SafetyAssessment
from ..simulation_engine.livability_evaluation import LivabilityEvaluation
from ..simulation_engine.cost_estimation import CostEstimation
from ..simulation_engine.pedestrian_flow import PedestrianFlowSimulation
from ..simulation_engine.blast_resistance_simulation import BlastResistanceSimulation
from ..fitness_evaluation.fitness_function import FitnessFunction

class EvolutionaryAlgorithm:
    def __init__(self, generations=100, population_size=100, mutation_rate=0.1, db_file="buildings.db"):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.population = [BuildingGenome() for _ in range(population_size)]
        self.generations = generations
        self.fitness_function = FitnessFunction()
        self.all_fitness_scores = []

    def evolve(self, progress_callback=None):
        for generation in range(self.generations):
            fitness_scores = self.evaluate_fitness()
            self.all_fitness_scores.extend(fitness_scores.tolist())
            
            best_fitness = np.max(fitness_scores, axis=0)
            avg_fitness = np.mean(fitness_scores, axis=0)
            
            if progress_callback:
                progress_callback(generation, best_fitness, avg_fitness)
          
            print(f"Generation {generation + 1}: Best Fitness = {best_fitness}, Avg Fitness = {avg_fitness}")

            if generation < self.generations - 1:  # Don't create offspring for the last generation
                offspring = self.create_offspring(fitness_scores)
                self.population = offspring
                
        final_fitness_scores = self.evaluate_fitness()
        best_index = np.argmax(np.mean(final_fitness_scores, axis=1))
        return self.population[best_index], final_fitness_scores 

    def evaluate_fitness(self):
        fitness_scores = []
        for genome in self.population:
            scores = self.evaluate_genome(genome)
            fitness_scores.append(scores)
        return np.array(fitness_scores)

    @staticmethod
    def evaluate_genome(genome):
        safety_score = SafetyAssessment(genome).assess()['overall_safety']
        structural_score = StructuralIntegrity(genome).analyse()['overall_integrity']
        livability_score = LivabilityEvaluation(genome).evaluate()['livability_score']
        energy_score = EnergySimulation(genome).simulate()['energy_efficiency']
        cost_score = CostEstimation(genome).estimate()['cost_score']
        pedestrian_flow_score = PedestrianFlowSimulation(genome).simulate()['evacuation_efficiency']
        blast_resistance_score = BlastResistanceSimulation(genome).simulate()['blast_resistance_score']
      
        print(f"All evaluations complete. Scores: safety={safety_score}, structural={structural_score}, "
                f"livability={livability_score}, energy={energy_score}, cost={cost_score}, "
                f"pedestrian_flow={pedestrian_flow_score}, blast_resistance={blast_resistance_score}")

        return np.array([safety_score, structural_score, livability_score, energy_score, cost_score, 
                pedestrian_flow_score, blast_resistance_score])
     
    def create_offspring(self, fitness_scores):
        offspring = []
        while len(offspring) < self.population_size:
            parent1 = self.tournament_selection(fitness_scores)
            parent2 = self.tournament_selection(fitness_scores)
            child = parent1.crossover(parent2)
            child.mutate(self.mutation_rate)
            offspring.append(child)
        return offspring

    def tournament_selection(self, fitness_scores, tournament_size=3):
        selected_indices = np.random.choice(len(self.population), tournament_size, replace=False)
        tournament_fitness = np.mean(fitness_scores[selected_indices], axis=1)  # Calculate average fitness for each individual
        winner_index = selected_indices[np.argmax(tournament_fitness)]
        return self.population[winner_index]



# Example use case
if __name__ == "__main__":
    ea = EvolutionaryAlgorithm(population_size=100)
    best_genome = ea.evolve()
    print(f"Best Genome: {best_genome}")
    
    # Evaluate the best genome
    best_scores, _, best_total_score = ea.fitness_function.evaluate(best_genome, ea.evaluate_genome)
    print("Best Genome Scores:")
    for key, value in best_scores.items():
        print(f"{key}: {value:.4f}")
    print(f"Total Score: {best_total_score:.4f}")