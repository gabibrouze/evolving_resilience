import unittest
import numpy as np
from src.ml_module.surrogate_model import SurrogateModel
from src.genetic_algorithm.encoding import BuildingGenome

class TestMLModule(unittest.TestCase):
    def setUp(self):
        self.surrogate_model = SurrogateModel()
        self.genomes = [BuildingGenome() for _ in range(100)]
        self.fitness_scores = np.random.rand(100, 7)

    def test_surrogate_model_training(self):
        self.surrogate_model.train(self.genomes, self.fitness_scores)
        self.assertTrue(self.surrogate_model.is_trained)

    def test_surrogate_model_prediction(self):
        self.surrogate_model.train(self.genomes, self.fitness_scores)
        test_genome = BuildingGenome()
        predictions = self.surrogate_model.predict(test_genome)
        self.assertEqual(len(predictions), 7)

    def test_feature_importance(self):
        self.surrogate_model.train(self.genomes, self.fitness_scores)
        importance = self.surrogate_model.feature_importance()
        self.assertEqual(len(importance), 7)

if __name__ == '__main__':
    unittest.main()