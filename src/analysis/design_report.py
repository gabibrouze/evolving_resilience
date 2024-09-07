# "src/analysis/design_report.py"

## The Design Report class has the following responsibilities:
## 1. Generate a detailed report of the building design based on the genome
## 2. Generate a summary table of the building design performance
## 3. Plot a radar chart of the building design performance
## 4. Save report as an Excel file

import pandas as pd
from ..simulation_engine.structural_integrity import StructuralIntegrity
from ..simulation_engine.energy_simulation import EnergySimulation
from ..simulation_engine.safety_assessment import SafetyAssessment
from ..simulation_engine.livability_evaluation import LivabilityEvaluation
from ..simulation_engine.cost_estimation import CostEstimation
from ..simulation_engine.pedestrian_flow import PedestrianFlowSimulation
from ..simulation_engine.blast_resistance_simulation import BlastResistanceSimulation

class DesignReport:
    def __init__(self, genome):
        self.genome = genome
        self.structural_analysis = StructuralIntegrity(genome)
        self.energy_simulation = EnergySimulation(genome)
        self.safety_assessment = SafetyAssessment(genome)
        self.livability_evaluation = LivabilityEvaluation(genome)
        self.cost_estimation = CostEstimation(genome)
        self.pedestrian_flow = PedestrianFlowSimulation(genome)
        self.blast_resistance = BlastResistanceSimulation(genome)

    def generate_report(self):
        report = {
            "Building Characteristics": self.get_building_characteristics(),
            "Structural Analysis": self.structural_analysis.analyse(),
            "Energy Efficiency": self.energy_simulation.simulate(),
            "Safety Assessment": self.safety_assessment.assess(),
            "Livability Evaluation": self.livability_evaluation.evaluate(),
            "Cost Estimation": self.cost_estimation.estimate(),
            "Pedestrian Flow": self.pedestrian_flow.simulate(),
            "Blast Resistance": self.blast_resistance.simulate()
        }
        return report

    def get_building_characteristics(self):
        return {
            "Height": self.genome.genes['building_envelope'].children[0].value,
            "Width": self.genome.genes['building_envelope'].children[1].value,
            "Length": self.genome.genes['building_envelope'].children[2].value,
            "Shape": self.genome.genes['building_envelope'].children[3].value,
            "Material": self.genome.genes['structural_system'].children[0].value,
            "Frame Type": self.genome.genes['structural_system'].children[1].value,
            "Number of Floors": self.genome.genes['floor_plans'].children[0].value,
            "Floor Height": self.genome.genes['floor_plans'].children[1].value,
            "HVAC Type": self.genome.genes['mep_systems'].children[0].value,
            "Renewable Energy": self.genome.genes['mep_systems'].children[3].value,
            "Window Ratio": self.genome.genes['facade'].children[0].value,
        }

    def generate_summary_table(self, report):
        summary = {
            "Structural Integrity": report["Structural Analysis"]["integrity_score"],
            "Energy Efficiency": report["Energy Efficiency"]["energy_efficiency"],
            "Safety Score": report["Safety Assessment"]["safety_score"],
            "Livability Score": report["Livability Evaluation"]["livability_score"],
            "Cost Score": report["Cost Estimation"]["cost_score"],
            "Evacuation Efficiency": report["Pedestrian Flow"]["evacuation_efficiency"],
            "Blast Resistance Score": report["Blast Resistance"]["blast_resistance_score"]
        }
        return pd.DataFrame([summary])

    def plot_performance_radar(self, ax):
        report = self.generate_report()
        categories = ['Structural', 'Energy', 'Safety', 'Livability', 'Cost', 'Evacuation', 'Blast Resistance']
        values = [
            report["Structural Analysis"]["integrity_score"],
            report["Energy Efficiency"]["energy_efficiency"],
            report["Safety Assessment"]["safety_score"],
            report["Livability Evaluation"]["livability_score"],
            report["Cost Estimation"]["cost_score"],
            report["Pedestrian Flow"]["evacuation_efficiency"],
            report["Blast Resistance"]["blast_resistance_score"]     
        ]

        angles = [n / float(len(categories)) * 2 * 3.141593 for n in range(len(categories))]
        values += values[:1]
        angles += angles[:1]

        ax.plot(angles, values)
        ax.fill(angles, values, alpha=0.3)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)
        ax.set_ylim(0, 1)
        ax.set_title("Building Performance Radar Chart")

    def save_report(self, output_path):
        report = self.generate_report()
        summary_table = self.generate_summary_table(report)

        with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
            # Write summary table
            summary_table.to_excel(writer, sheet_name='Summary', index=False)

            # Write detailed report
            pd.DataFrame([report]).to_excel(writer, sheet_name='Detailed Report', index=False)

            # Add performance radar chart
            workbook = writer.book
            worksheet = writer.sheets['Summary']
            chart = workbook.add_chart({'type': 'radar'})
            chart.add_series({
                'categories': ['Summary', 0, 0, 0, 6],
                'values': ['Summary', 1, 0, 1, 6],
            })
            chart.set_title({'name': 'Building Performance Radar Chart'})
            worksheet.insert_chart('D2', chart)

        print(f"Report saved to {output_path}")

# Example use case
if __name__ == "__main__":
    from ..genetic_algorithm.encoding import BuildingGenome
    
    genome = BuildingGenome()
    report_generator = DesignReport(genome)
    report_generator.save_report("building_design_report.xlsx")