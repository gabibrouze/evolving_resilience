# "src/simulation_engine/blast_resistance_simulation.py"

## Implements the `BlastResistanceSimulation` class with detailed blast resistance simulation, which includes:
## - Peak pressure
## - Positive phase duration
## - Mass calculation
## - Stiffness calculation
## - Building dynamics
## - Damage index calculation
## - Blast resistance simulation

import numpy as np
from scipy.integrate import odeint

class BlastResistanceSimulation:
    def __init__(self, genome):
        self.genome = genome
        self.height = genome.genes['building_envelope'].children[0].value
        self.width = genome.genes['building_envelope'].children[1].value
        self.length = genome.genes['building_envelope'].children[2].value
        self.material = genome.genes['structural_system'].children[0].value
        self.frame_type = genome.genes['structural_system'].children[1].value

    def simulate(self):
        peak_pressure = 1000  # kPa
        positive_phase_duration = 0.02  # seconds

        mass = self.calculate_mass()
        stiffness = self.calculate_stiffness()

        t = np.linspace(0, 0.5, 1000)
        y0 = [0, 0]  # Initial displacement and velocity
        sol = odeint(self.building_dynamics, y0, t, args=(mass, stiffness, peak_pressure, positive_phase_duration))

        max_displacement = np.max(np.abs(sol[:, 0]))
        max_velocity = np.max(np.abs(sol[:, 1]))

        damage_index = self.calculate_damage_index(max_displacement)

        return {
            "max_displacement": max_displacement,
            "max_velocity": max_velocity,
            "damage_index": damage_index,
            "blast_resistance_score": 1 - damage_index  # Higher score means better resistance
        }

    def calculate_mass(self):
        volume = self.height * self.width * self.length
        if self.material == 'concrete':
            density = 2400  # kg/m^3
        elif self.material == 'steel':
            density = 7850  # kg/m^3
        else:  # wood
            density = 500  # kg/m^3
        return volume * density

    def calculate_stiffness(self):
        if self.material == 'concrete':
            elastic_modulus = 30e9  # Pa
        elif self.material == 'steel':
            elastic_modulus = 200e9  # Pa
        else:  # wood
            elastic_modulus = 11e9  # Pa

        moment_of_inertia = (self.width * self.length**3) / 12
        if self.frame_type == 'moment frame':
            factor = 1
        elif self.frame_type == 'braced frame':
            factor = 1.5
        else:  # shear wall
            factor = 2

        return factor * (3 * elastic_modulus * moment_of_inertia) / (self.height**3)

    def building_dynamics(self, y, t, m, k, p0, td):
        x, dx = y
        if t <= td:
            f = p0 * (1 - t/td) * self.width * self.length
        else:
            f = 0
        ddx = (f - k * x) / m
        return [dx, ddx]

    def calculate_damage_index(self, max_displacement):
        yield_displacement = 0.1  # Assumed yield displacement
        ultimate_displacement = 0.5  # Assumed ultimate displacement
        if max_displacement < yield_displacement:
            return 0
        elif max_displacement > ultimate_displacement:
            return 1
        else:
            return (max_displacement - yield_displacement) / (ultimate_displacement - yield_displacement)

# Example use case
if __name__ == "__main__":
    from ..genetic_algorithm.encoding import BuildingGenome
    
    genome = BuildingGenome()
    blast_resistance = BlastResistanceSimulation(genome)
    print("Blast Resistance:", blast_resistance.simulate())