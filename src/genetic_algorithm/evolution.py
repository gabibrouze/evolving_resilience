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
from ..db.database import Database
from ..fitness_evaluation.fitness_function import FitnessFunction

class EvolutionaryAlgorithm:
    def __init__(self, generations=100, population_size=100, mutation_rate=0.1, db_file="buildings.db"):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.population = [BuildingGenome() for _ in range(population_size)]
        self.generations = generations
        self.fitness_function = FitnessFunction()
        self.db = Database(db_file)

    def evolve(self, progress_callback=None):
        print("Starting evolution...")
        for generation in range(self.generations):
            print(f"Generation {generation} starting...")
            fitness_scores = self.evaluate_fitness()
            print(f"Fitness scores calculated: {fitness_scores}")
            
            # Select parents and create offspring
            offspring = self.create_offspring(fitness_scores)
            
            # Replace the old population with the new offspring
            self.population = offspring
            
            # Save the best genome and optimisation history
            best_genome = self.population[np.argmax(fitness_scores)]
            best_fitness = np.max(fitness_scores)
            avg_fitness = np.mean(fitness_scores)
            
            self.db.save_building(best_genome, best_fitness)
            self.db.save_optimisation_history(generation, best_fitness, avg_fitness)
            
            if progress_callback:
                progress_callback.emit(generation, best_fitness, avg_fitness)
            
            print(f"Generation {generation + 1}: Best Fitness = {best_fitness:.4f}, Avg Fitness = {avg_fitness:.4f}")
        
        return self.population[np.argmax(self.evaluate_fitness())]

    def evaluate_fitness(self):
        fitness_scores = []
        for i, genome in enumerate(self.population):
            try:
                print(f"Evaluating genome {i+1}/{len(self.population)}")
                _, _, total_score = self.fitness_function.evaluate(genome, self.evaluate_genome)
                fitness_scores.append(total_score)
                print(f"Genome {i+1} fitness: {total_score}")
            except Exception as e:
                print(f"Error evaluating genome {i+1}: {str(e)}")
                print(traceback.format_exc())
                fitness_scores.append(0)  # Assign a zero fitness score to failed evaluations
        return np.array(fitness_scores)

    # def evaluate_fitness(self):
    #     fitness_scores = []
    #     for genome in self.population:
    #         _, _, total_score = self.fitness_function.evaluate(genome, self.evaluate_genome)
    #         fitness_scores.append(total_score)
    #     return np.array(fitness_scores)\

    @staticmethod
    def evaluate_genome(genome):
        try:
            print("Starting SafetyAssessment...")
            safety_score = SafetyAssessment(genome).assess()['overall_safety']
            print(f"SafetyAssessment complete. Score: {safety_score}")

            print("Starting StructuralIntegrity analysis...")
            structural_score = StructuralIntegrity(genome).analyse()['overall_integrity']
            print(f"StructuralIntegrity analysis complete. Score: {structural_score}")

            print("Starting LivabilityEvaluation...")
            livability_score = LivabilityEvaluation(genome).evaluate()['livability_score']
            print(f"LivabilityEvaluation complete. Score: {livability_score}")

            print("Starting EnergySimulation...")
            energy_score = EnergySimulation(genome).simulate()['energy_efficiency']
            print(f"EnergySimulation complete. Score: {energy_score}")

            print("Starting CostEstimation...")
            cost_score = CostEstimation(genome).estimate()['cost_score']
            print(f"CostEstimation complete. Score: {cost_score}")

            print("Starting PedestrianFlowSimulation...")
            pedestrian_flow_score = PedestrianFlowSimulation(genome).simulate()['evacuation_efficiency']
            print(f"PedestrianFlowSimulation complete. Score: {pedestrian_flow_score}")

            print("Starting BlastResistanceSimulation...")
            blast_resistance_score = BlastResistanceSimulation(genome).simulate()['blast_resistance_score']
            print(f"BlastResistanceSimulation complete. Score: {blast_resistance_score}")

            print(f"All evaluations complete. Scores: safety={safety_score}, structural={structural_score}, "
                  f"livability={livability_score}, energy={energy_score}, cost={cost_score}, "
                  f"pedestrian_flow={pedestrian_flow_score}, blast_resistance={blast_resistance_score}")

            return [safety_score, structural_score, livability_score, energy_score, cost_score, 
                    pedestrian_flow_score, blast_resistance_score]
        except Exception as e:
            print(f"Error in evaluate_genome: {str(e)}")
            print(traceback.format_exc())
            return [0, 0, 0, 0, 0, 0, 0]  # Return zero scores if evaluation fails


    # @staticmethod
    # def evaluate_genome(genome):
    #     try:
    #         safety_score = SafetyAssessment(genome).assess()['overall_safety']
    #         structural_score = StructuralIntegrity(genome).analyse()['overall_integrity']
    #         livability_score = LivabilityEvaluation(genome).evaluate()['livability_score']
    #         energy_score = EnergySimulation(genome).simulate()['energy_efficiency']
    #         cost_score = CostEstimation(genome).estimate()['cost_score']
    #         pedestrian_flow_score = PedestrianFlowSimulation(genome).simulate()['evacuation_efficiency']
    #         blast_resistance_score = BlastResistanceSimulation(genome).simulate()['blast_resistance_score']
            
    #         print(f"Individual scores: safety={safety_score}, structural={structural_score}, "
    #               f"livability={livability_score}, energy={energy_score}, cost={cost_score}, "
    #               f"pedestrian_flow={pedestrian_flow_score}, blast_resistance={blast_resistance_score}")
            
    #         return [safety_score, structural_score, livability_score, energy_score, cost_score, 
    #                 pedestrian_flow_score, blast_resistance_score]
    #     except Exception as e:
    #         print(f"Error in evaluate_genome: {str(e)}")
    #         print(traceback.format_exc())
    #         return [0, 0, 0, 0, 0, 0, 0]  # Return zero scores if evaluation fails


    # @staticmethod
    # def evaluate_genome(genome):
    #     safety_score = SafetyAssessment(genome).assess()['overall_safety']
    #     structural_score = StructuralIntegrity(genome).analyse()['overall_integrity']
    #     livability_score = LivabilityEvaluation(genome).evaluate()['livability_score']
    #     energy_score = EnergySimulation(genome).simulate()['energy_efficiency']
    #     cost_score = CostEstimation(genome).estimate()['cost_score']
    #     pedestrian_flow_score = PedestrianFlowSimulation(genome).simulate()['evacuation_efficiency']
    #     blast_resistance_score = BlastResistanceSimulation(genome).simulate()['blast_resistance_score']
        
    #     print("Safety:", safety_score)
    #     print("Structural:", structural_score)
    #     print("Livability:", livability_score)
    #     print("Energy:", energy_score)
    #     print("Cost:", cost_score)
    #     print("Pedestrian Flow:", pedestrian_flow_score)
    #     print("Blast Resistance:", blast_resistance_score)

    #     return [safety_score, structural_score, livability_score, energy_score, cost_score, pedestrian_flow_score, blast_resistance_score]

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
        tournament_fitness = fitness_scores[selected_indices]
        winner_index = selected_indices[np.argmax(tournament_fitness)]
        return self.population[winner_index]

    def __del__(self):
        self.db.close()

# Example use case
if __name__ == "__main__":
    ea = EvolutionaryAlgorithm(population_size=100)
    best_genome = ea.evolve()
    print("Best Genome:")
    print(best_genome)
    
    # Evaluate the best genome
    best_scores, _, best_total_score = ea.fitness_function.evaluate(best_genome, ea.evaluate_genome)
    print("Best Genome Scores:")
    for key, value in best_scores.items():
        print(f"{key}: {value:.4f}")
    print(f"Total Score: {best_total_score:.4f}")