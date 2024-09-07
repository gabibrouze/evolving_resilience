# "src/simulation_engine/safety_assessment.py"

## Implements the `SafetyAssessment` class with detailed safety assessment, which includes:
## - Fire safety
## - Structural safety
## - Emergency exit safety
## - Hazardous material safety
## - Security measures
## - Earthquake safety
## - Flood safety
## - Wind safety

import numpy as np
import traceback

class SafetyAssessment:
    def __init__(self, genome):
        self.genome = genome

    def assess(self):
        try:
            print("SafetyAssessment: Starting assessment...")
            # Perform detailed safety assessment
            fire_safety = self.assess_fire_safety()
            structural_safety = self.assess_structural_safety()
            emergency_exit_safety = self.assess_emergency_exit_safety()
            hazardous_material_safety = self.assess_hazardous_material_safety()
            security_measures = self.assess_security_measures()
            earthquake_safety = self.assess_earthquake_safety()
            flood_safety = self.assess_flood_safety()
            wind_safety = self.assess_wind_safety()

            overall_safety = (
                fire_safety * 0.3 +
                structural_safety * 0.3 +
                emergency_exit_safety * 0.1 +
                hazardous_material_safety * 0.1 +
                security_measures * 0.05 +
                earthquake_safety * 0.05 +
                flood_safety * 0.05 +
                wind_safety * 0.05
            )

            print(f"SafetyAssessment: Assessment complete. Overall safety score: {overall_safety}")

            return {
                "overall_safety": overall_safety,
                "fire_safety": fire_safety,
                "structural_safety": structural_safety,
                "emergency_exit_safety": emergency_exit_safety,
                "hazardous_material_safety": hazardous_material_safety,
                "security_measures": security_measures,
                "earthquake_safety": earthquake_safety,
                "flood_safety": flood_safety,
                "wind_safety": wind_safety
            }
        except Exception as e:
            print(f"Error in SafetyAssessment: {str(e)}")
            print(traceback.format_exc())
            return {"overall_safety": 0}  # Return a zero safety score if assessment fails


    def assess_fire_safety(self):
        material = self.genome.genes['structural_system'].children[0].value
        num_floors = self.genome.genes['floor_plans'].children[0].value
        
        if material == 'concrete':
            base_score = 0.8
        elif material == 'steel':
            base_score = 0.7
        else:  # wood
            base_score = 0.5

        # Adjust for number of floors, more floors = harder to evacuate
        floor_factor = max(0, 1 - (num_floors - 5) * 0.02)
        
        return base_score * floor_factor

    def assess_structural_safety(self):
        height = self.genome.genes['building_envelope'].children[0].value
        material = self.genome.genes['structural_system'].children[0].value
        frame_type = self.genome.genes['structural_system'].children[1].value
       
        if material == 'concrete':
            base_score = 0.8
        elif material == 'steel':
            base_score = 0.9
        else:  # wood
            base_score = 0.6

        if frame_type == 'moment frame':
            frame_factor = 0.9
        elif frame_type == 'braced frame':
            frame_factor = 1.0
        else:  # shear wall
            frame_factor = 1.1
        
        # Adjust for height, taller buildings = more vulnerable
        height_factor = max(0, 1 - (height - 20) * 0.005)

        return base_score * frame_factor * height_factor

    def assess_emergency_exit_safety(self):
        num_floors = self.genome.genes['floor_plans'].children[0].value
        length = self.genome.genes['building_envelope'].children[2].value
        width = self.genome.genes['building_envelope'].children[1].value
      
        area = width * length
        num_exits = max(2, int(np.sqrt(area) / 10))  # Assumption: 1 exit per 100 m^2, min = 2

        exit_factor = min(1, num_exits / (num_floors / 2))  # Ideal: 2 exits per floor
        
        return exit_factor

    def assess_hazardous_material_safety(self):
        # TODO: assume generally good hazardous material practices
        return np.random.uniform(0.7, 1.0)

    def assess_security_measures(self):
        # TODO: assume varying levels of security measures
        return np.random.uniform(0.6, 1.0)

    def assess_earthquake_safety(self):
        frame_type = self.genome.genes['structural_system'].children[1].value
        height = self.genome.genes['building_envelope'].children[0].value

        if frame_type == 'moment frame':
            base_score = 0.7
        elif frame_type == 'braced frame':
            base_score = 0.8
        else:  # shear wall
            base_score = 0.9

        # Adjust for height, taller buildings = more vulnerable
        height_factor = max(0, 1 - (height - 20) * 0.005)
        
        return base_score * height_factor

    def assess_flood_safety(self):
        height = self.genome.genes['building_envelope'].children[0].value
        # Assumption: 20m is maximum flood height
        return min(1, height / 20)

    def assess_wind_safety(self):
        height = self.genome.genes['building_envelope'].children[0].value
        shape = self.genome.genes['building_envelope'].children[3].value

        if shape == 'rectangular':
            base_score = 0.7
        elif shape == 'L-shaped':
            base_score = 0.8
        else:  # U-shaped
            base_score = 0.9

        # Adjust for height, taller buildings = more exposed to wind
        height_factor = max(0, 1 - (height - 50) * 0.005)
        
        return base_score * height_factor

# Example use case
if __name__ == "__main__":
    from ..genetic_algorithm.encoding import BuildingGenome
    
    genome = BuildingGenome()
    safety_assessment = SafetyAssessment(genome)
    print("Safety Assessment:", safety_assessment.assess())