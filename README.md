# Evolving Resilience: AI-Driven Architectural Solutions for High-Risk Areas

## Overview

This project implements an AI-driven evolutionary design system that generates optimised building designs for high-risk environments. It uses genetic algorithms and machine learning to evolve designs that balance safety, structural integrity, livability, and energy efficiency.

## Features

- Evolutionary algorithm for building design optimisation
- Multi-objective fitness evaluation
- 3D visualisation of building designs
- Pareto front visualisation for multi-objective optimisation
- Integration with Building Information Modeling (BIM) through IFC import/export
- Detailed design report generation
- Database storage for evolved designs and optimisation history

## Installation

1. Clone the repository:

`git clone https://github.com/gabibrouze/evolving-resilience.git`

`cd evolving-resilience`

2. Create and activate a virtual environment:

`python -m venv venv`

`source venv/bin/activate`

3. Install the required packages:

`pip install -r requirements.txt`

## Usage

1. Run the main application:

`python main.py`

2. Use the GUI to set evolutionary parameters, start the evolution process, and visualise results.

3. Import/export designs using the IFC format for BIM integration.

4. Generate detailed reports of evolved designs.

## Using the Surrogate Model

The Surrogate Model can be used to quickly estimate fitness scores without running full simulations. Here's how to use it:

1. Train the model:
   ```python
   from src.ml_module.surrogate_model import SurrogateModel
   from src.genetic_algorithm.evolution import EvolutionaryAlgorithm

   ea = EvolutionaryAlgorithm(population_size=100)
   genomes = ea.population
   fitness_scores = ea.evaluate_fitness()

   surrogate = SurrogateModel()
   surrogate.train(genomes, fitness_scores)
   ```
2. Use the trained model to predict fitness scores:
    ```python
    test_genome = BuildingGenome()
    predicted_fitness = surrogate.predict(test_genome)
    ```

3. Analyse feature importance
    ```python
    importance = surrogate.feature_importance()
    for objective, imp in importance.items():
    print(f"\nFeature importance for {objective}:")
    for feature, score in sorted(imp.items(), key=lambda x: x[1], reverse=True):
        print(f"{feature}: {score:.4f}")
    ```

The Surrogate Model can be integrated into the evolutionary process to speed up fitness evaluations, especially in later generations.

## Using NSGA-II for Multi-Objective Optimization

NSGA-II (Non-dominated Sorting Genetic Algorithm II) is implemented for multi-objective optimisation of building designs. Here's how to use it:

1. Initialise and run the NSGA-II algorithm:
   ```python
   from src.genetic_algorithm.nsga_ii import NSGAII

   nsga_ii = NSGAII(population_size=100)
   best_genome = nsga_ii.evolve()
   ```

2. The `evolve` method will run the algorithm for the specified number of generations (default is 100). It performs the following steps in each generation:

- Evaluate fitness
- Create offspring
- Combine parents and offspring
- Perform non-dominated sorting
- Calculate crowding distance
- Select the next generation

3. After evolution, you can access the Pareto front (non-dominated solutions) from the population attribute:

    ```python
    pareto_front = nsga_ii.population
    ```

4. You can customise the objectives and their evaluation in the evaluate_genome method of the NSGAII class.

NSGA-II is useful when dealing with conflicting objectives, as it provides a set of Pareto-optimal solutions rather than a single "best" solution.

To use NSGA-II in the genetic algorithm: replace the standard evolutionary algorithm with NSGA-II. i.e., modify the the evolution loop to use NSGA-II instead of a single-objective genetic algorithm.

## Project Structure

- `src/`: Source code for the project
- `genetic_algorithm/`: Implementation of the evolutionary algorithm
- `simulation_engine/`: Various simulation modules for evaluating building performance
- `visualisation/`: Modules for 3D building visualization and Pareto front plots
- `bim_integration/`: IFC import/export functionality
- `ui/`: User interface implementation
- `db/`: Database operations for storing and retrieving designs
- `analysis/`: Design report generation
- `tests/`: Unit tests for the project
- `docs/`: Documentation including API reference and user manual

## Running Tests

To run the unit tests, execute the following command from the project root directory:

`python -m unittest discover tests`

This will run all the tests in the `tests` directory.
