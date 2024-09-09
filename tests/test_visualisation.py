import unittest
import matplotlib.pyplot as plt
from src.visualisation.building_visualiser import BuildingVisualiser
from src.visualisation.pareto_front_visualiser import ParetoFrontVisualiser
from src.genetic_algorithm.encoding import BuildingGenome
import numpy as np

class TestVisualisation(unittest.TestCase):
    def setUp(self):
        self.genome = BuildingGenome()
        self.building_visualiser = BuildingVisualiser(self.genome)
        self.pareto_visualiser = ParetoFrontVisualiser(None, np.random.rand(100, 7))

    def test_building_visualiser(self):
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        self.building_visualiser.visualise(ax)
        self.assertIsNotNone(ax.get_title())
        plt.close(fig)

    def test_pareto_front_visualiser_2d(self):
        fig, ax = plt.subplots()
        self.pareto_visualiser.visualise_2d(ax)
        self.assertIsNotNone(ax.get_title())
        plt.close(fig)

    def test_pareto_front_visualiser_3d(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        self.pareto_visualiser.visualise_3d(ax)
        self.assertIsNotNone(ax.get_title())
        plt.close(fig)

if __name__ == '__main__':
    unittest.main()