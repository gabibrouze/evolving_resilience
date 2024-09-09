import unittest
import os
from src.bim_integration.ifc_interface import IFCInterface
from src.genetic_algorithm.encoding import BuildingGenome

class TestBIMIntegration(unittest.TestCase):
    def setUp(self):
        self.ifc_interface = IFCInterface()
        self.genome = BuildingGenome()

    def test_export_to_ifc(self):
        output_path = "test_export.ifc"
        self.ifc_interface.export_to_ifc(self.genome, output_path)
        self.assertTrue(os.path.exists(output_path))
        os.remove(output_path)

    # # def test_import_from_ifc(self):
    # #     sample_ifc_path = "test_import.ifc"
    # #     self.ifc_interface.export_to_ifc(self.genome, sample_ifc_path)
        
    # #     imported_genome = self.ifc_interface.import_from_ifc(sample_ifc_path)
    # #     self.assertIsInstance(imported_genome, BuildingGenome)
        
    #     os.remove(sample_ifc_path)

if __name__ == '__main__':
    unittest.main()