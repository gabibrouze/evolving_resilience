# "src/simulation_engine/livability_evaluation.py"

## Implements the `LivabilityEvaluation` class with detailed livability evaluation, which includes:
## - Spatial quality
## - Natural light
## - Thermal comfort
## - Acoustic comfort
## - Air quality

class LivabilityEvaluation:
    def __init__(self, genome):
        self.genome = genome

    def evaluate(self):
        # Extract relevant parameters from the genome
        height = self.genome.genes['building_envelope'].children[0].value
        width = self.genome.genes['building_envelope'].children[1].value
        length = self.genome.genes['building_envelope'].children[2].value
        shape = self.genome.genes['building_envelope'].children[3].value
        num_floors = self.genome.genes['floor_plans'].children[0].value
        floor_height = self.genome.genes['floor_plans'].children[1].value
        window_ratio = self.genome.genes['facade'].children[0].value
        hvac_type = self.genome.genes['mep_systems'].children[0].value

        # Evaluate various aspects of livability
        spatial_quality = self._evaluate_spatial_quality(width, length, floor_height, shape)
        natural_light = self._evaluate_natural_light(window_ratio, shape)
        thermal_comfort = self._evaluate_thermal_comfort(hvac_type, window_ratio)
        acoustic_comfort = self._evaluate_acoustic_comfort(num_floors, shape)
        air_quality = self._evaluate_air_quality(hvac_type, window_ratio)

        # Calculate overall livability score
        livability_score = (spatial_quality + natural_light + thermal_comfort + acoustic_comfort + air_quality) / 5

        return {
            'livability_score': livability_score,
            'spatial_quality': spatial_quality,
            'natural_light': natural_light,
            'thermal_comfort': thermal_comfort,
            'acoustic_comfort': acoustic_comfort,
            'air_quality': air_quality
        }

    def _evaluate_spatial_quality(self, width, length, floor_height, shape):
        area = width * length
        volume = area * floor_height
        
        # Assumption: ideal area is between 50-200 sq meters
        area_score = 1 - min(abs(area - 125) / 75, 1)
         
        # Assumption: ideal volume is between 150-600 cubic meters
        volume_score = 1 - min(abs(volume - 375) / 225, 1)

        # Shape factor
        if shape == 'rectangular':
            shape_score = 0.8
        elif shape == 'L-shaped':
            shape_score = 0.9
        else:  # U-shaped
            shape_score = 1.0

        return (area_score + volume_score + shape_score) / 3

    def _evaluate_natural_light(self, window_ratio, shape):
        # Assumption: ideal window ratio is between 0.3-0.6
        light_score = 1 - min(abs(window_ratio - 0.45) / 0.15, 1)

        # Shape factor for light distribution
        if shape == 'rectangular':
            shape_score = 0.9
        elif shape == 'L-shaped':
            shape_score = 0.8
        else:  # U-shaped
            shape_score = 0.7

        return (light_score + shape_score) / 2

    def _evaluate_thermal_comfort(self, hvac_type, window_ratio):
        if hvac_type == 'central':
            hvac_score = 0.9
        elif hvac_type == 'distributed':
            hvac_score = 0.8
        else:  # hybrid
            hvac_score = 1.0

        # Window ratio affects thermal comfort
        # Assumption: 0.3-0.5 is ideal
        window_score = 1 - min(abs(window_ratio - 0.4) / 0.1, 1)

        return (hvac_score + window_score) / 2

    def _evaluate_acoustic_comfort(self, num_floors, shape):
        # Assumption: more floors = more noise
        floor_factor = max(0, 1 - (num_floors - 5) * 0.05)

        if shape == 'rectangular':
            shape_score = 0.8
        elif shape == 'L-shaped':
            shape_score = 0.9
        else:  # U-shaped
            shape_score = 1.0  # U-shape creates quieter inner spaces

        return (floor_factor + shape_score) / 2

    def _evaluate_air_quality(self, hvac_type, window_ratio):
        if hvac_type == 'central':
            hvac_score = 0.8
        elif hvac_type == 'distributed':
            hvac_score = 0.7
        else:  # hybrid
            hvac_score = 0.9

        # Higher window ratio allows for better natural ventilation
        window_score = min(window_ratio / 0.5, 1)

        return (hvac_score + window_score) / 2


# Example use case
if __name__ == "__main__":
    from ..genetic_algorithm.encoding import BuildingGenome
    
    genome = BuildingGenome()
    livability_evaluation = LivabilityEvaluation(genome)
    print("Livability Evaluation:", livability_evaluation.evaluate())