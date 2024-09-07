# "tests/test_simulation_engine.py"

import unittest
from src.genetic_algorithm.encoding import BuildingGenome
from src.simulation_engine.structural_integrity import StructuralIntegrity
from src.simulation_engine.energy_simulation import EnergySimulation
from src.simulation_engine.safety_assessment import SafetyAssessment
from src.simulation_engine.livability_evaluation import LivabilityEvaluation
from src.simulation_engine.cost_estimation import CostEstimation
from src.simulation_engine.pedestrian_flow import PedestrianFlowSimulation
from src.simulation_engine.blast_resistance_simulation import BlastResistanceSimulation

class TestSimulationEngine(unittest.TestCase):
    def setUp(self):
        self.genome = BuildingGenome()

    def test_structural_integrity(self):
        si = StructuralIntegrity(self.genome)
        result = si.analyse()
        self.assertIn('overall_integrity', result)
        self.assertTrue(0 <= result['overall_integrity'] <= 1)

    def test_energy_simulation(self):
        es = EnergySimulation(self.genome)
        result = es.simulate()
        self.assertIn('energy_efficiency', result)
        self.assertTrue(0 <= result['energy_efficiency'] <= 1)

    def test_safety_assessment(self):
        sa = SafetyAssessment(self.genome)
        result = sa.assess()
        self.assertIn('overall_safety', result)
        self.assertTrue(0 <= result['overall_safety'] <= 1)

    def test_livability_evaluation(self):
        le = LivabilityEvaluation(self.genome)
        result = le.evaluate()
        self.assertIn('livability_score', result)
        self.assertTrue(0 <= result['livability_score'] <= 1)

    def test_cost_estimation(self):
        ce = CostEstimation(self.genome)
        result = ce.estimate()
        self.assertIn('cost_score', result)
        self.assertTrue(0 <= result['cost_score'] <= 1)

    def test_pedestrian_flow(self):
        pf = PedestrianFlowSimulation(self.genome)
        result = pf.simulate()
        self.assertIn('evacuation_efficiency', result)
        self.assertTrue(0 <= result['evacuation_efficiency'] <= 1)

    def test_blast_resistance(self):
        br = BlastResistanceSimulation(self.genome)
        result = br.simulate()
        self.assertIn('blast_resistance_score', result)
        self.assertTrue(0 <= result['blast_resistance_score'] <= 1)

if __name__ == '__main__':
    unittest.main()