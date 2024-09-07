# "src/simulation_engine/cost_estimation.py"

## Implements the `CostEstimation` class with detailed cost estimation, which includes:
## - Material costs
## - Labour costs
## - MEP costs
## - Finishing costs
## - Total cost estimation

class CostEstimation:
    def __init__(self, genome):
        self.genome = genome
        self.material_costs = {
            'concrete': 100,  # £/m^3
            'steel': 2000,    # £/ton
            'wood': 500       # £/m^3
        }
        self.labour_cost = 50  # £/hour

    def estimate(self):
        height = self.genome.genes['building_envelope'].children[0].value
        width = self.genome.genes['building_envelope'].children[1].value
        length = self.genome.genes['building_envelope'].children[2].value
        material = self.genome.genes['structural_system'].children[0].value
        frame_type = self.genome.genes['structural_system'].children[1].value
        num_floors = self.genome.genes['floor_plans'].children[0].value
        hvac_type = self.genome.genes['mep_systems'].children[0].value
        renewable_energy = self.genome.genes['mep_systems'].children[3].value

        volume = height * width * length
        material_cost = self._estimate_material_cost(volume, material)
        labour_cost = self._estimate_labour_cost(volume, frame_type)
        mep_cost = self._estimate_mep_cost(volume, hvac_type, renewable_energy)
        finishing_cost = self._estimate_finishing_cost(volume)

        total_cost = material_cost + labour_cost + mep_cost + finishing_cost
        floor_area = width * length * num_floors
        cost_per_sqm = total_cost / floor_area

        # Normalize cost score (Assumption: £2000/sqm is average)
        cost_score = max(0, 1 - (cost_per_sqm - 2000) / 1000)

        return {
            'total_cost': total_cost,
            'cost_per_sqm': cost_per_sqm,
            'cost_score': cost_score,
            'material_cost': material_cost,
            'labour_cost': labour_cost,
            'mep_cost': mep_cost,
            'finishing_cost': finishing_cost
        }

    def _estimate_material_cost(self, volume, material):
        if material == 'steel':
            # Assumption: 100kg of steel per cubic meter of building
            return (volume * 0.1) * self.material_costs[material]
        else:
            return volume * self.material_costs[material]

    def _estimate_labour_cost(self, volume, frame_type):
        if frame_type == 'moment frame':
            labour_hours = volume * 0.5
        elif frame_type == 'braced frame':
            labour_hours = volume * 0.4
        else:  # shear wall
            labour_hours = volume * 0.3
        
        return labour_hours * self.labour_cost

    def _estimate_mep_cost(self, volume, hvac_type, renewable_energy):
        base_cost = volume * 50  # £50 per cubic meter for MEP systems
        
        if hvac_type == 'central':
            hvac_factor = 1.2
        elif hvac_type == 'distributed':
            hvac_factor = 1.0
        else:  # hybrid
            hvac_factor = 1.1
        
        renewable_factor = 1.3 if renewable_energy else 1.0
        
        return base_cost * hvac_factor * renewable_factor

    def _estimate_finishing_cost(self, volume):
        return volume * 100  # £100 per cubic meter for finishing

# Example use case
if __name__ == "__main__":
    from ..genetic_algorithm.encoding import BuildingGenome
    
    genome = BuildingGenome()
    cost_estimation = CostEstimation(genome)
    print("Cost Estimation:", cost_estimation.estimate())