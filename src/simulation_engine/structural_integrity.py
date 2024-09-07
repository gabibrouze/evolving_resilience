# "src/simulation_engine/simulation_engine.py"

## Implements the `StructuralIntegrity` class with detailed structural analysis, which includes:
## - Lateral stability
## - Vertical load capacity
## - Foundation stability
## - Seismic performance
## - Wind resistance

class StructuralIntegrity:
    def __init__(self, genome):
        self.genome = genome

    def analyse(self):
        # Extract relevant parameters from the genome
        height = self.genome.genes['building_envelope'].children[0].value
        width = self.genome.genes['building_envelope'].children[1].value
        length = self.genome.genes['building_envelope'].children[2].value
        material = self.genome.genes['structural_system'].children[0].value
        frame_type = self.genome.genes['structural_system'].children[1].value

        # Perform detailed structural analysis
        lateral_stability = self.assess_lateral_stability(height, width, length, material, frame_type)
        vertical_load_capacity = self.assess_vertical_load_capacity(height, width, length, material)
        foundation_stability = self.assess_foundation_stability(width, length, material)
        seismic_performance = self.assess_seismic_performance(height, material, frame_type)
        wind_resistance = self.assess_wind_resistance(height, width, length, material, frame_type)

        # Calculate overall structural integrity
        overall_integrity = (
            lateral_stability * 0.25 +
            vertical_load_capacity * 0.25 +
            foundation_stability * 0.2 +
            seismic_performance * 0.15 +
            wind_resistance * 0.15
        )

        return {
            "overall_integrity": overall_integrity,
            "lateral_stability": lateral_stability,
            "vertical_load_capacity": vertical_load_capacity,
            "foundation_stability": foundation_stability,
            "seismic_performance": seismic_performance,
            "wind_resistance": wind_resistance
        }

    def assess_lateral_stability(self, height, width, length, material, frame_type):
        aspect_ratio = height / min(width, length)
        if aspect_ratio > 5:
            base_score = 0.5
        elif aspect_ratio > 3:
            base_score = 0.7
        else:
            base_score = 0.9

        if frame_type == 'moment frame':
            frame_factor = 0.9
        elif frame_type == 'braced frame':
            frame_factor = 1.0
        else:  # shear wall
            frame_factor = 1.1

        if material == 'steel':
            material_factor = 1.1
        elif material == 'concrete':
            material_factor = 1.0
        else:  # wood
            material_factor = 0.8

        return base_score * frame_factor * material_factor

    def assess_vertical_load_capacity(self, height, width, length, material):
        volume = height * width * length
        if material == 'concrete':
            density = 2400  # kg/m^3
            strength = 30e6  # Pa
        elif material == 'steel':
            density = 7850  # kg/m^3
            strength = 250e6  # Pa
        else:  # wood
            density = 500  # kg/m^3
            strength = 20e6  # Pa

        mass = volume * density
        load_capacity = strength * width * length
        safety_factor = load_capacity / (mass * 9.81)

        return min(1, safety_factor / 3)  # Assumption: ideal safety factor = 3

    def assess_foundation_stability(self, width, length, material):
        area = width * length
        if material == 'concrete':
            base_pressure = 300e3  # Pa
        elif material == 'steel':
            base_pressure = 250e3  # Pa
        else:  # wood
            base_pressure = 150e3  # Pa

        foundation_capacity = area * base_pressure
        estimated_building_weight = area * 5000  # Rough estimate: 5000 N/m^2

        safety_factor = foundation_capacity / estimated_building_weight
        return min(1, safety_factor / 2)  # Assumption: ideal safety factor of 2

    def assess_seismic_performance(self, height, material, frame_type):
        if frame_type == 'moment frame':
            base_score = 0.7
        elif frame_type == 'braced frame':
            base_score = 0.8
        else:  # shear wall
            base_score = 0.9

        if material == 'steel':
            material_factor = 1.1
        elif material == 'concrete':
            material_factor = 1.0
        else:  # wood
            material_factor = 0.8

        height_factor = max(0, 1 - (height - 20) * 0.005)

        return base_score * material_factor * height_factor

    def assess_wind_resistance(self, height, width, length, material, frame_type):
        aspect_ratio = height / min(width, length)
        if aspect_ratio > 5:
            base_score = 0.6
        elif aspect_ratio > 3:
            base_score = 0.8
        else:
            base_score = 1.0

        if frame_type == 'moment frame':
            frame_factor = 0.9
        elif frame_type == 'braced frame':
            frame_factor = 1.0
        else:  # shear wall
            frame_factor = 1.1

        if material == 'steel':
            material_factor = 1.1
        elif material == 'concrete':
            material_factor = 1.0
        else:  # wood
            material_factor = 0.8

        return base_score * frame_factor * material_factor


# Example use case
if __name__ == "__main__":
    from ..genetic_algorithm.encoding import BuildingGenome
    
    genome = BuildingGenome()
    structural_analysis = StructuralIntegrity(genome)
    print("Structural Integrity:", structural_analysis.analyse())