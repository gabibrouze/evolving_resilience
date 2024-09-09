import unittest
import os
from src.analysis.design_report import DesignReport
from src.genetic_algorithm.encoding import BuildingGenome

class TestAnalysis(unittest.TestCase):
    def setUp(self):
        self.genome = BuildingGenome()
        self.report_generator = DesignReport(self.genome)

    def test_generate_report(self):
        report = self.report_generator.generate_report()
        self.assertIsInstance(report, dict)
        self.assertIn('Building Characteristics', report)

    def test_generate_summary_table(self):
        report = self.report_generator.generate_report()
        summary_table = self.report_generator.generate_summary_table(report)
        self.assertEqual(len(summary_table), 1)

    def test_save_report(self):
        output_path = "test_report.xlsx"
        self.report_generator.save_report(output_path)
        self.assertTrue(os.path.exists(output_path))
        os.remove(output_path)

if __name__ == '__main__':
    unittest.main()