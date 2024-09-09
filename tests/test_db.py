import unittest
import os
from src.db.database import Database
from src.genetic_algorithm.encoding import BuildingGenome

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db_file = "test_buildings.db"
        self.db = Database(self.db_file)
        self.genome = BuildingGenome()
        self.fitness_scores = [0.8, 0.7, 0.9, 0.6, 0.5, 0.8, 0.7]

    def tearDown(self):
        self.db.close()
        if os.path.exists(self.db_file):
            os.remove(self.db_file)

    def test_save_and_get_building(self):
        building_id = self.db.save_building(self.genome, self.fitness_scores)
        retrieved_building = self.db.get_building(building_id)
        self.assertIsNotNone(retrieved_building)
        self.assertIsInstance(retrieved_building['genome'], BuildingGenome)

    def test_save_and_get_optimisation_history(self):
        self.db.save_optimisation_history(1, [0.9, 0.8, 0.7], [0.7, 0.6, 0.5])
        history = self.db.get_optimisation_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]['generation'], 1)

if __name__ == '__main__':
    unittest.main()