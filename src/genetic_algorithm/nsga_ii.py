# "src/genetic_algorithm/nsga_ii.py"

## NSGA-II Algorithm: Non-dominated Sorting Genetic Algorithm II (NSGA-II) 
## Implements the NSGA-II algorithm to optimide a building design based on multiple objectives such as:
## - structural integrity
## - energy efficiency 
## - safety
## - livability
## - cost
## - pedestrian flow
## - blast resistance

## sources:
## - https://www.sciencedirect.com/topics/computer-science/non-dominated-sorting-genetic-algorithm-ii
## - https://ieeexplore.ieee.org/document/996017

import numpy as np
from .encoding import BuildingGenome
from ..simulation_engine.structural_integrity import StructuralIntegrity
from ..simulation_engine.energy_simulation import EnergySimulation
from ..simulation_engine.safety_assessment import SafetyAssessment
from ..simulation_engine.livability_evaluation import LivabilityEvaluation
from ..simulation_engine.cost_estimation import CostEstimation
from ..simulation_engine.pedestrian_flow import PedestrianFlowSimulation
from ..simulation_engine.blast_resistance_simulation import BlastResistanceSimulation

class NSGAII:
    def __init__(self, population_size=100, mutation_rate=0.1):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.population = [BuildingGenome() for _ in range(population_size)]
        self.generations = 100

    def evolve(self):
        for generation in range(self.generations):
            # 1. Evaluate fitness   
            fitness_scores = self.evaluate_fitness()
            # 2. Create offspring
            offspring = self.create_offspring()
            # 3. Combine parents and offspring
            combined_population = self.population + offspring
            # 4. Non-dominated sorting
            fronts = self.fast_non_dominated_sort(combined_population)
            # 5. Calculate crowding distance
            self.calculate_crowding_distance(fronts)
            # 6. Select next generation
            self.population = self.select_next_generation(fronts)

            # Print generation stats
            self.print_generation_stats(generation, fitness_scores)

        return self.population[0]  # Return the best individual

    def evaluate_fitness(self):
        fitness_scores = []
        for genome in self.population:
            scores = self.evaluate_genome(genome)
            fitness_scores.append(scores)
        return np.array(fitness_scores)

    def evaluate_genome(self, genome):
        structural_integrity = StructuralIntegrity(genome).analyse()['structural_integrity']
        energy_efficiency = EnergySimulation(genome).simulate()['energy_efficiency']
        safety_score = SafetyAssessment(genome).assess()['safety_score']
        livability_score = LivabilityEvaluation(genome).evaluate()['livability_score']
        cost_score = CostEstimation(genome).estimate()['cost_score']
        pedestrian_flow_score = PedestrianFlowSimulation(genome).simulate()['evacuation_efficiency']
        blast_resistance_score = BlastResistanceSimulation(genome).simulate()['blast_resistance_score']
        
        return [structural_integrity, energy_efficiency, safety_score, livability_score, cost_score, pedestrian_flow_score, blast_resistance_score]

    def create_offspring(self):
        offspring = []
        while len(offspring) < self.population_size:
            parent1, parent2 = np.random.choice(self.population, 2, replace=False)
            child = parent1.crossover(parent2)
            child.mutate(self.mutation_rate)
            offspring.append(child)
        return offspring

    def fast_non_dominated_sort(self, population):
        domination_counts = np.zeros(len(population))
        dominated_solutions = [[] for _ in range(len(population))]
        fronts = [[]]
  
        for i, p in enumerate(population):
            for j, q in enumerate(population):
                if i != j:
                    if self.dominates(p, q):
                        dominated_solutions[i].append(j)
                    elif self.dominates(q, p):
                        domination_counts[i] += 1
            
            if domination_counts[i] == 0:
                fronts[0].append(i)
        
        i = 0
        while fronts[i]:
            next_front = []
            for p in fronts[i]:
                for q in dominated_solutions[p]:
                    domination_counts[q] -= 1
                    if domination_counts[q] == 0:
                        next_front.append(q)
            i += 1
            fronts.append(next_front)

        return fronts[:-1]  # Remove the last empty front

    def dominates(self, p, q):
        p_scores = self.evaluate_genome(p)
        q_scores = self.evaluate_genome(q)
        return all(p_scores[i] >= q_scores[i] for i in range(len(p_scores))) and any(p_scores[i] > q_scores[i] for i in range(len(p_scores)))

    def calculate_crowding_distance(self, fronts):
        for front in fronts:
            if len(front) > 2:
                for obj in range(len(self.evaluate_genome(self.population[0]))):
                    front_sorted = sorted(front, key=lambda x: self.evaluate_genome(self.population[x])[obj])
                    self.population[front_sorted[0]].crowding_distance = float('inf')
                    self.population[front_sorted[-1]].crowding_distance = float('inf')
                    obj_range = (
                        self.evaluate_genome(self.population[front_sorted[-1]])[obj] -
                        self.evaluate_genome(self.population[front_sorted[0]])[obj]
                    )
                    for i in range(1, len(front_sorted) - 1):
                        prev_obj = self.evaluate_genome(self.population[front_sorted[i-1]])[obj]
                        next_obj = self.evaluate_genome(self.population[front_sorted[i+1]])[obj]
                        if obj_range == 0:
                            self.population[front_sorted[i]].crowding_distance += 0
                        else:
                            self.population[front_sorted[i]].crowding_distance += (next_obj - prev_obj) / obj_range

    def select_next_generation(self, fronts):
        next_gen = []
        for front in fronts:
            if len(next_gen) + len(front) <= self.population_size:
                next_gen.extend([self.population[i] for i in front])
            else:
                remaining = self.population_size - len(next_gen)
                sorted_front = sorted(front, key=lambda x: self.population[x].crowding_distance, reverse=True)
                next_gen.extend([self.population[i] for i in sorted_front[:remaining]])
                break
        return next_gen

    def print_generation_stats(self, generation, fitness_scores):
        avg_scores = np.mean(fitness_scores, axis=0)
        best_scores = np.max(fitness_scores, axis=0)
        print(f"Generation {generation}:")
        objectives = ["Structural Integrity", "Energy Efficiency", "Safety", "Livability", "Cost", "Pedestrian Flow", "Blast Resistance"]
        for i, obj in enumerate(objectives):
            print(f"  {obj}: Avg = {avg_scores[i]:.4f}, Best = {best_scores[i]:.4f}")

# Example use of the NSGA-II algorithm
if __name__ == "__main__":
    nsga_ii = NSGAII(population_size=100)
    best_genome = nsga_ii.evolve()
    print("Best Genome:")
    print(best_genome)