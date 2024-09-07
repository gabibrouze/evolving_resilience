# "src/genetic_algorithm/evolution.py"

## Implements the `EvolutionaryAlgorithm` class, including methods for:
## - Evaluating fitness
## - Tournament selection
## - Evolving the population

import numpy as np
from .encoding import BuildingGenome
from ..simulation_engine.structural_integrity import StructuralIntegrity
from ..simulation_engine.energy_simulation import EnergySimulation
from ..simulation_engine.safety_assessment import SafetyAssessment
from ..simulation_engine.livability_evaluation import LivabilityEvaluation
from ..simulation_engine.cost_estimation import CostEstimation
from ..simulation_engine.pedestrian_flow import PedestrianFlowSimulation
from ..simulation_engine.blast_resistance_simulation import BlastResistanceSimulation
from ..db.database import Database
from ..fitness_evaluation.fitness_function import FitnessFunction

class EvolutionaryAlgorithm:
    def __init__(self, population_size=100, mutation_rate=0.1, db_file="buildings.db"):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.population = [BuildingGenome() for _ in range(population_size)]
        self.generations = 100
        self.db = Database(db_file)
        self.fitness_function = FitnessFunction()

    def evolve(self):
        for generation in range(self.generations):
            fitness_scores = self.evaluate_fitness()
            new_population = []
            
            for _ in range(self.population_size):
                parent1, parent2 = self.tournament_selection(fitness_scores)
                child = parent1.crossover(parent2)
                child.mutate(self.mutation_rate)
                new_population.append(child)
            
            self.population = new_population
            
            best_genome = self.population[np.argmax(fitness_scores)]
            best_fitness = np.max(fitness_scores)
            avg_fitness = np.mean(fitness_scores)
            print(f"Generation {generation + 1}: Best Fitness = {best_fitness:.4f}, Avg Fitness = {avg_fitness:.4f}")

            self.db.save_building(best_genome, best_fitness)
            self.db.save_optimisation_history(generation, best_fitness, avg_fitness)
        
        best_index = np.argmax(fitness_scores)
        return self.population[best_index]
    
    def evaluate_fitness(self):
        fitness_scores = []
        for genome in self.population:
            _, _, total_score = self.fitness_function.evaluate(genome)
            fitness_scores.append(total_score)
        return fitness_scores
    
    @staticmethod
    def evaluate_genome(genome):
        # This method returns a list of individual scores for each objective
        safety_score = EvolutionaryAlgorithm.evaluate_safety(genome)
        structural_score = EvolutionaryAlgorithm.evaluate_structural_integrity(genome)
        livability_score = EvolutionaryAlgorithm.evaluate_livability(genome)
        energy_score = EvolutionaryAlgorithm.evaluate_energy_efficiency(genome)
        cost_score = EvolutionaryAlgorithm.evaluate_cost(genome)
        pedestrian_flow_score = EvolutionaryAlgorithm.evaluate_pedestrian_flow(genome)
        blast_resistance_score = EvolutionaryAlgorithm.evaluate_blast_resistance(genome)
        
        return [safety_score, structural_score, livability_score, energy_score, cost_score, pedestrian_flow_score, blast_resistance_score]

    
    def tournament_selection(self, fitness_scores, tournament_size=3):
        selected_indices = np.random.choice(len(self.population), tournament_size, replace=False)
        tournament_fitness = fitness_scores[selected_indices]
        winner_index = selected_indices[np.argmax(tournament_fitness)]
        return self.population[winner_index]
    
    @staticmethod
    def evaluate_safety(self, genome):
        safety_assessment = SafetyAssessment(genome)
        results = safety_assessment.assess()
        return results['overall_safety']
    
    @staticmethod
    def evaluate_structural_integrity(self, genome):
        structural_analysis = StructuralIntegrity(genome)
        results = structural_analysis.analyse()
        return results['overall_integrity']

    @staticmethod
    def evaluate_livability(self, genome):
        livability_evaluation = LivabilityEvaluation(genome)
        results = livability_evaluation.evaluate()
        return results['livability_score']
    
    @staticmethod
    def evaluate_energy_efficiency(self, genome):
        energy_simulation = EnergySimulation(genome)
        results = energy_simulation.simulate()
        return results['energy_efficiency']
    
    @staticmethod
    def evaluate_cost(self, genome):
        cost_estimation = CostEstimation(genome)
        results = cost_estimation.estimate()
        return results['cost_score']

    @staticmethod
    def evaluate_pedestrian_flow(self, genome):
        pedestrian_flow = PedestrianFlowSimulation(genome)
        results = pedestrian_flow.simulate()
        return results['evacuation_efficiency']

    @staticmethod
    def evaluate_blast_resistance(self, genome):
        blast_resistance = BlastResistanceSimulation(genome)
        results = blast_resistance.simulate()
        return results['blast_resistance_score']

    def __del__(self):
        self.db.close()
        
# Main entry point
if __name__ == "__main__":
    ea = EvolutionaryAlgorithm(population_size=100)
    best_genome = ea.evolve()
    print("Best Genome:")
    print(best_genome)