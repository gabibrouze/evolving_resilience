# "src/ui/main_window.py"

## This file contains the main window of the application, 
## which is a PyQt5 GUI that allows the user with the following functionality:
## - Control panel for setting evolution parameters (population size, generations, mutation rate)
## - Start button to begin the evolutionary process
## - Import and export buttons for IFC files
## - Generate report button to create a detailed design report
## - Progress label to show the current status of the evolution
## - 3D building visualisation tab for visualising the evolved building
## - Pareto front visualisation
## - Performance radar chart
## - Detailed results text view
## - Load a saved design by entering the building ID

import sys
import json
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSpinBox, QDoubleSpinBox, QFileDialog, QSlider, QTabWidget, QTextEdit, QMessageBox, QInputDialog
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from ..genetic_algorithm.evolution import EvolutionaryAlgorithm
from ..visualisation.building_visualiser import BuildingVisualiser
from ..visualisation.pareto_front_visualiser import ParetoFrontVisualiser
from ..bim_integration.ifc_interface import IFCInterface
from ..analysis.design_report import DesignReport
from ..db.database import Database
from ..fitness_evaluation.fitness_function import FitnessFunction
from ..encoder_decoder.encoder import Encoder
from ..encoder_decoder.decoder import Decoder

class EvolutionThread(QThread):
    update_progress = pyqtSignal(int, object, object)
    evolution_complete = pyqtSignal(object, object)

    def __init__(self, ea):
        QThread.__init__(self)
        self.ea = ea

    def run(self):
        best_genome, fitness_scores = self.ea.evolve(self.progress_callback)
        # fitness_scores = self.ea.evaluate_fitness()
        self.evolution_complete.emit(best_genome, fitness_scores)

    def progress_callback(self, generation, best_fitness, avg_fitness):
        self.update_progress.emit(generation, best_fitness, avg_fitness)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Evolving Resilience - AI-Driven Architectural Solutions for High-Risk Areas")
        self.setGeometry(100, 100, 1200, 800)
        self.db = Database("buildings.db")
        self.encoder = Encoder()
        self.decoder = Decoder()

        self.fitness_function = FitnessFunction()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Control Panel
        control_panel = QWidget()
        control_layout = QVBoxLayout(control_panel)
        
        self.population_size_spin = QSpinBox()
        self.population_size_spin.setRange(10, 1000)
        self.population_size_spin.setValue(100)
        control_layout.addWidget(QLabel("Population Size:"))
        control_layout.addWidget(self.population_size_spin)

        self.generations_spin = QSpinBox()
        self.generations_spin.setRange(1, 1000)
        self.generations_spin.setValue(100)
        control_layout.addWidget(QLabel("Generations:"))
        control_layout.addWidget(self.generations_spin)

        self.mutation_rate_spin = QDoubleSpinBox()
        self.mutation_rate_spin.setRange(0, 1)
        self.mutation_rate_spin.setSingleStep(0.01)
        self.mutation_rate_spin.setValue(0.1)
        control_layout.addWidget(QLabel("Mutation Rate:"))
        control_layout.addWidget(self.mutation_rate_spin)

        self.load_design_button = QPushButton("Load Saved Design")
        self.load_design_button.clicked.connect(self.load_saved_design)
        control_layout.addWidget(self.load_design_button)

        self.start_button = QPushButton("Start Evolution")
        self.start_button.clicked.connect(self.start_evolution)
        control_layout.addWidget(self.start_button)

        self.import_ifc_button = QPushButton("Import IFC")
        self.import_ifc_button.clicked.connect(self.import_ifc)
        control_layout.addWidget(self.import_ifc_button)

        self.export_ifc_button = QPushButton("Export IFC")
        self.export_ifc_button.clicked.connect(self.export_ifc)
        self.export_ifc_button.setEnabled(False)
        control_layout.addWidget(self.export_ifc_button)

        self.generate_report_button = QPushButton("Generate Report")
        self.generate_report_button.clicked.connect(self.generate_report)
        self.generate_report_button.setEnabled(False)
        control_layout.addWidget(self.generate_report_button)

        self.progress_label = QLabel("Progress: Not Started")
        control_layout.addWidget(self.progress_label)

        # Add weight adjustment sliders
        self.weight_sliders = {}
        for objective in self.fitness_function.weights.keys():
            slider = QSlider(Qt.Horizontal)
            slider.setRange(0, 100)
            slider.setValue(int(self.fitness_function.weights[objective] * 100))
            slider.valueChanged.connect(self.update_weights)
            control_layout.addWidget(QLabel(f"{objective.capitalize()} Weight:"))
            control_layout.addWidget(slider)
            self.weight_sliders[objective] = slider

        main_layout.addWidget(control_panel)

        # Visualisation and Results Panel
        results_panel = QTabWidget()
        
        # 3D Visualisation Tab
        self.figure_3d = Figure(figsize=(8, 6), dpi=100)
        self.canvas_3d = FigureCanvas(self.figure_3d)
        results_panel.addTab(self.canvas_3d, "3D Visualisation")

        # Pareto Front Tab
        self.figure_pareto = Figure(figsize=(8, 6), dpi=100)
        self.canvas_pareto = FigureCanvas(self.figure_pareto)
        results_panel.addTab(self.canvas_pareto, "Pareto Front")

        # Performance Radar Tab
        self.figure_radar = Figure(figsize=(8, 6), dpi=100)
        self.canvas_radar = FigureCanvas(self.figure_radar)
        results_panel.addTab(self.canvas_radar, "Performance Radar")

        # Detailed Results Tab
        self.detailed_results = QTextEdit()
        self.detailed_results.setReadOnly(True)
        results_panel.addTab(self.detailed_results, "Detailed Results")

        main_layout.addWidget(results_panel)

        self.ea = None
        self.evolution_thread = None
        self.best_genome = None
        self.fitness_scores = None
        self.ifc_interface = IFCInterface()

    def start_evolution(self):
        population_size = self.population_size_spin.value()
        generations = self.generations_spin.value()
        mutation_rate = self.mutation_rate_spin.value()
        
        print(f"Generations: {generations}, Population Size: {population_size}, Mutation Rate: {mutation_rate}")
        self.ea = EvolutionaryAlgorithm(population_size=population_size, 
                                        mutation_rate=mutation_rate,
                                        generations=generations)

        self.evolution_thread = EvolutionThread(self.ea)
        self.evolution_thread.update_progress.connect(self.update_progress)
        self.evolution_thread.evolution_complete.connect(self.evolution_complete)
        self.evolution_thread.start()

        self.start_button.setEnabled(False)
        self.import_ifc_button.setEnabled(False)
        self.export_ifc_button.setEnabled(False)
        self.generate_report_button.setEnabled(False)
        self.progress_label.setText("Evolution in progress...")

    def update_progress(self, generation, best_fitness, avg_fitness):
        # Save optimisation history in the main thread
        self.db.save_optimisation_history(generation, best_fitness, avg_fitness)
        best_fitness_str = ", ".join([f"{x:.2f}" for x in best_fitness])
        avg_fitness_str = ", ".join([f"{x:.2f}" for x in avg_fitness])
        self.progress_label.setText(f"Generation: {generation + 1}\nBest Fitness: [{best_fitness_str}]\nAvg Fitness: [{avg_fitness_str}]")
       
    def evolution_complete(self, best_genome, fitness_scores):
        self.start_button.setEnabled(True)
        self.import_ifc_button.setEnabled(True)
        self.export_ifc_button.setEnabled(True)
        self.generate_report_button.setEnabled(True)
        self.progress_label.setText("Evolution Complete")
        self.best_genome = best_genome
        self.fitness_scores = fitness_scores
        # Find the index of the best genome based on mean fitness
        best_index = np.argmax(np.mean(fitness_scores, axis=1))
        # Save the best genome with its fitness scores
        self.db.save_building(best_genome, fitness_scores[best_index])
        self.update_visualisations()

    def update_visualisations(self, from_db=False):
        # Update 3D Visualisation
        self.figure_3d.clear()
        ax_3d = self.figure_3d.add_subplot(111, projection='3d')
        visualiser = BuildingVisualiser(self.best_genome)
        visualiser.visualise(ax_3d)
        self.canvas_3d.draw()

        # Update Pareto Front
        self.figure_pareto.clear()
        ax_pareto = self.figure_pareto.add_subplot(221)
        ax_pareto_3d = self.figure_pareto.add_subplot(222, projection='3d')
        ax_parallel = self.figure_pareto.add_subplot(223)
        ax_radar = self.figure_pareto.add_subplot(224, projection='polar')
        
        if not from_db and self.ea and hasattr(self.ea, 'population') and hasattr(self.ea, 'all_fitness_scores'):
            pareto_visualiser = ParetoFrontVisualiser(self.ea.population, np.array(self.ea.all_fitness_scores))
            pareto_visualiser.visualise_2d(ax_pareto)
            pareto_visualiser.visualise_3d(ax_pareto_3d)
            pareto_visualiser.visualise_parallel_coordinates(ax_parallel)
            pareto_visualiser.visualise_radar_chart(ax_radar)
        else:
            # Display "No evolution data" message
            ax_pareto.text(0.5, 0.5, "No evolution data", horizontalalignment='center', verticalalignment='center', fontsize=12)
            ax_pareto.axis('off')
            ax_pareto_3d.text2D(0.5, 0.5, "No evolution data", horizontalalignment='center', verticalalignment='center', fontsize=12, transform=ax_pareto_3d.transAxes)
            ax_pareto_3d.axis('off')
            ax_parallel.text(0.5, 0.5, "No evolution data", horizontalalignment='center', verticalalignment='center', fontsize=12)
            ax_parallel.axis('off')
            ax_radar.text(0.5, 0.5, "No evolution data", horizontalalignment='center', verticalalignment='center', fontsize=12)
            ax_radar.axis('off')
            
        self.figure_pareto.tight_layout()
        self.canvas_pareto.draw()

        # Update Performance Radar
        self.figure_radar.clear()
        ax_radar = self.figure_radar.add_subplot(111, projection='polar')
        report_generator = DesignReport(self.best_genome)
        report = report_generator.generate_report()
        report_generator.plot_performance_radar(ax_radar)
        self.canvas_radar.draw()

        # Update Detailed Results
        self.detailed_results.setText(str(report))
            
    def import_ifc(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Import IFC File", "", "IFC Files (*.ifc)")
        if file_path:
            try:
                imported_genome = self.ifc_interface.import_from_ifc(file_path)
                self.best_genome = imported_genome
                self.update_visualisations()
                self.export_ifc_button.setEnabled(True)
                self.generate_report_button.setEnabled(True)
            except Exception as e:
                QMessageBox.critical(self, "Import Error", f"Error importing IFC: {str(e)}")

    def export_ifc(self):
        if self.best_genome:
            file_path, _ = QFileDialog.getSaveFileName(self, "Export IFC File", "", "IFC Files (*.ifc)")
            if file_path:
                try:
                    self.ifc_interface.export_to_ifc(self.best_genome, file_path)
                    QMessageBox.information(self, "Export Successful", "IFC Export Successful")
                except Exception as e:
                    QMessageBox.critical(self, "Export Error", f"Error exporting IFC: {str(e)}")
        else:
            QMessageBox.warning(self, "No Data", "No genome available for export")

    def generate_report(self):
        if self.best_genome:
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Report", "", "Excel Files (*.xlsx)")
            if file_path:
                try:
                    report_generator = DesignReport(self.best_genome)
                    report_generator.save_report(file_path)
                    QMessageBox.information(self, "Report Generated", "Report Generated Successfully")
                except Exception as e:
                    QMessageBox.critical(self, "Report Error", f"Error generating report: {str(e)}")
        else:
            QMessageBox.warning(self, "No Data", "No genome available for report generation")

    def load_saved_design(self):
        building_id, ok = QInputDialog.getInt(self, "Load Saved Design", "Enter Building ID:")
        if ok:
            building = self.db.get_building(building_id)
            if building:
                self.best_genome = building['genome']
                self.fitness_scores = building['fitness_scores']
                self.ea = None  # Clear the evolutionary algorithm data
                self.update_visualisations(from_db=True)
                self.export_ifc_button.setEnabled(True)
                self.generate_report_button.setEnabled(True)
            else:
                QMessageBox.warning(self, "Not Found", f"No building found with ID {building_id}")

    def update_weights(self):
        new_weights = {obj: slider.value() / 100 for obj, slider in self.weight_sliders.items()}
        total = sum(new_weights.values())
        normalized_weights = {obj: weight / total for obj, weight in new_weights.items()}
        self.fitness_function.update_weights(normalized_weights)
        if self.ea:
            self.ea.fitness_function = self.fitness_function

    def import_design(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Import Design", "", "JSON Files (*.json)")
        if file_path:
            with open(file_path, 'r') as f:
                architectural_design = json.load(f)
            genome = self.encoder.encode(architectural_design)
            self.best_genome = genome
            self.update_visualisations()

    def export_design(self):
        if self.best_genome:
            file_path, _ = QFileDialog.getSaveFileName(self, "Export Design", "", "JSON Files (*.json)")
            if file_path:
                architectural_design = self.decoder.decode(self.best_genome)
                with open(file_path, 'w') as f:
                    json.dump(architectural_design, f, indent=2)
                QMessageBox.information(self, "Export Successful", "Design exported successfully")
        else:
            QMessageBox.warning(self, "No Data", "No genome available for export")

    def __del__(self):
        self.db.close()

    def closeEvent(self, event):
        self.db.close()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


