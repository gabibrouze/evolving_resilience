import unittest
from src.fitness_evaluation.fitness_function import FitnessFunction
from src.genetic_algorithm.encoding import BuildingGenome

class TestFitnessEvaluation(unittest.TestCase):
    def setUp(self):
        self.fitness_function = FitnessFunction()
        self.genome = BuildingGenome()

    def test_fitness_evaluation(self):
        scores, weighted_scores, total_score = self.fitness_function.evaluate(self.genome, lambda x: [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5])
        self.assertIsInstance(scores, dict)
        self.assertIsInstance(weighted_scores, dict)
        self.assertIsInstance(total_score, float)

    def test_weight_update(self):
        new_weights = {'safety': 0.5, 'cost': 0.5}
        self.fitness_function.update_weights(new_weights)
        self.assertEqual(self.fitness_function.weights['safety'], 0.5)
        self.assertEqual(self.fitness_function.weights['cost'], 0.5)

if __name__ == '__main__':
    unittest.main()