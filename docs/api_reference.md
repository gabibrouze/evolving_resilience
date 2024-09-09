# API Reference

## Genetic Algorithm

### `class EvolutionaryAlgorithm`

The main class for running the evolutionary algorithm.

#### Methods:

- `__init__(self, population_size=100, mutation_rate=0.1, generations=100)`
- `evolve(self, progress_callback=None)`
- `evaluate_fitness(self)`
- `create_offspring(self, fitness_scores)`

## Simulation Engine

### `class StructuralIntegrity`

Evaluates the structural integrity of a building design.

#### Methods:

- `__init__(self, genome)`
- `analyse(self)`

### `class EnergySimulation`

Simulates the energy efficiency of a building design.

#### Methods:

- `__init__(self, genome)`
- `simulate(self)`

## Visualisation

### `class BuildingVisualiser`

Provides 3D Visualisation of building designs.

#### Methods:

- `__init__(self, genome)`
- `visualise(self, ax)`

### `class ParetoFrontVisualiser`

Visualizes the Pareto front for multi-objective optimization.

#### Methods:

- `__init__(self, population, fitness_scores)`
- `visualise_2d(self, ax, obj1=0, obj2=1)`
- `visualise_3d(self, ax, obj1=0, obj2=1, obj3=2)`

