# "src/encoder_decoder/encoder.py"

## Implements the `Encoder` class, which encodes an architectural design into a `BuildingGenome` object.

from ..genetic_algorithm.encoding import BuildingGenome, HierarchicalGene

class Encoder:
    def __init__(self):
        self.encoding_schemes = {
            'building_envelope': self.encode_building_envelope,
            'structural_system': self.encode_structural_system,
            'floor_plans': self.encode_floor_plans,
            'mep_systems': self.encode_mep_systems,
            'facade': self.encode_facade
        }

    def encode(self, architectural_design):
        genome = BuildingGenome()
        for key, encode_func in self.encoding_schemes.items():
            genome.genes[key] = encode_func(architectural_design[key])
        return genome

    def encode_building_envelope(self, envelope_data):
        return HierarchicalGene('building_envelope', None, [
            HierarchicalGene('height', envelope_data['height']),
            HierarchicalGene('width', envelope_data['width']),
            HierarchicalGene('length', envelope_data['length']),
            HierarchicalGene('shape', envelope_data['shape']),
        ])

    def encode_structural_system(self, structural_data):
        return HierarchicalGene('structural_system', None, [
            HierarchicalGene('material', structural_data['material']),
            HierarchicalGene('frame_type', structural_data['frame_type']),
        ])

    def encode_floor_plans(self, floor_data):
        return HierarchicalGene('floor_plans', None, [
            HierarchicalGene('num_floors', floor_data['num_floors']),
            HierarchicalGene('floor_height', floor_data['floor_height']),
        ])

    def encode_mep_systems(self, mep_data):
        return HierarchicalGene('mep_systems', None, [
            HierarchicalGene('hvac_type', mep_data['hvac_type']),
            HierarchicalGene('lighting_type', mep_data['lighting_type']),
            HierarchicalGene('plumbing_type', mep_data['plumbing_type']),
            HierarchicalGene('renewable_energy', mep_data['renewable_energy']),
        ])

    def encode_facade(self, facade_data):
        return HierarchicalGene('facade', None, [
            HierarchicalGene('window_ratio', facade_data['window_ratio']),
            HierarchicalGene('material', facade_data['material']),
        ])

# Example use case
if __name__ == "__main__":
    architectural_design = {
        'building_envelope': {
            'height': 30,
            'width': 20,
            'length': 40,
            'shape': 'rectangular'
        },
        'structural_system': {
            'material': 'concrete',
            'frame_type': 'moment frame'
        },
        'floor_plans': {
            'num_floors': 5,
            'floor_height': 3
        },
        'mep_systems': {
            'hvac_type': 'central',
            'lighting_type': 'LED',
            'plumbing_type': 'central',
            'renewable_energy': True
        },
        'facade': {
            'window_ratio': 0.4,
            'material': 'glass'
        }
    }

    encoder = Encoder()
    genome = encoder.encode(architectural_design)
    print(genome)