# "tests/test_genetic_algorithm.py"

import unittest
from src.genetic_algorithm.encoding import BuildingGenome, HierarchicalGene
from src.genetic_algorithm.evolution import EvolutionaryAlgorithm
from src.genetic_algorithm.nsga_ii import NSGAII

class TestBuildingGenome(unittest.TestCase):
    def setUp(self):
        self.genome = BuildingGenome()

    def test_initialization(self):
        self.assertIsInstance(self.genome.genes['building_envelope'], HierarchicalGene)
        self.assertIsInstance(self.genome.genes['structural_system'], HierarchicalGene)
        self.assertIsInstance(self.genome.genes['floor_plans'], HierarchicalGene)
        self.assertIsInstance(self.genome.genes['mep_systems'], HierarchicalGene)
        self.assertIsInstance(self.genome.genes['facade'], HierarchicalGene)

    def test_mutate(self):
        original_values = {k: v.value for k, v in self.genome.genes.items()}
        self.genome.mutate(mutation_rate=1.0)  # Force mutation
        new_values = {k: v.value for k, v in self.genome.genes.items()}
        self.assertNotEqual(original_values, new_values)

    def test_crossover(self):
        parent1 = BuildingGenome()
        parent2 = BuildingGenome()
        child = parent1.crossover(parent2)
        self.assertIsInstance(child, BuildingGenome)
        self.assertNotEqual(child.genes, parent1.genes)
        self.assertNotEqual(child.genes, parent2.genes)

class TestEvolutionaryAlgorithm(unittest.TestCase):
    def setUp(self):
        self.ea = EvolutionaryAlgorithm(population_size=10, generations=5)

    def test_initialization(self):
        self.assertEqual(len(self.ea.population), 10)
        self.assertEqual(self.ea.generations, 5)

    def test_evolve(self):
        best_genome = self.ea.evolve()
        self.assertIsInstance(best_genome, BuildingGenome)

class TestNSGAII(unittest.TestCase):
    def setUp(self):
        self.nsga_ii = NSGAII(population_size=10)

    def test_initialization(self):
        self.assertEqual(len(self.nsga_ii.population), 10)

    def test_fast_non_dominated_sort(self):
        fronts = self.nsga_ii.fast_non_dominated_sort(self.nsga_ii.population)
        self.assertIsInstance(fronts, list)
        self.assertTrue(all(isinstance(front, list) for front in fronts))

    def test_calculate_crowding_distance(self):
        front = self.nsga_ii.population[:5]
        self.nsga_ii.calculate_crowding_distance([front])
        self.assertTrue(all(hasattr(ind, 'crowding_distance') for ind in front))

if __name__ == '__main__':
    unittest.main()