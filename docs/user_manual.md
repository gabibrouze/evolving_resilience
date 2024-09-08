# User Manual

## Getting Started

1. Launch the application by running `python main.py`.
2. The main window will appear with controls on the left and visualisation tabs on the right.

## Setting Evolution Parameters

1. Use the spinboxes to set:
   - Population Size
   - Number of Generations
   - Mutation Rate
2. Adjust the objective weights using the sliders.

## Running the Evolution

1. Click the "Start Evolution" button to begin the optimisation process.
2. The progress will be displayed in the progress label.
3. Once complete, the best design will be visualised and results will be shown in the tabs.

## Visualising Results

- 3D Visualisation: Shows a 3D model of the best building design.
- Pareto Front: Displays the Pareto front of the multi-objective optimisation.
- Performance Radar: Shows a radar chart of the building's performance across different objectives.
- Detailed Results: Provides a text report of the building's characteristics and performance.

## Importing/Exporting Designs

1. Use the "Import IFC" button to load a building design from an IFC file.
2. Use the "Export IFC" button to save the current best design as an IFC file.

## Generating Reports

1. Click the "Generate Report" button to create a detailed Excel report of the current best design.
2. Choose a location to save the report file.

## Loading Saved Designs

1. Click the "Load Saved Design" button.
2. Enter the ID of the saved design you wish to load.

## Tips for Optimal Use

- Start with a smaller population size and fewer generations for quick results, then increase for more thorough optimisation.
- Adjust objective weights to focus the evolution on specific aspects of building performance.
- Use the Pareto front visualisation to understand trade-offs between different objectives.