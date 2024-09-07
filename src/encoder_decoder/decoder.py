# "src/encoder_decoder/decoder.py"

## Implements the `Decoder` class, which decodes a `BuildingGenome` object into an architectural design.

class Decoder:
    def __init__(self):
        self.decoding_schemes = {
            'building_envelope': self.decode_building_envelope,
            'structural_system': self.decode_structural_system,
            'floor_plans': self.decode_floor_plans,
            'mep_systems': self.decode_mep_systems,
            'facade': self.decode_facade
        }

    def decode(self, genome):
        architectural_design = {}
        for key, decode_func in self.decoding_schemes.items():
            architectural_design[key] = decode_func(genome.genes[key])
        return architectural_design

    def decode_building_envelope(self, gene):
        return {
            'height': gene.children[0].value,
            'width': gene.children[1].value,
            'length': gene.children[2].value,
            'shape': gene.children[3].value
        }

    def decode_structural_system(self, gene):
        return {
            'material': gene.children[0].value,
            'frame_type': gene.children[1].value
        }

    def decode_floor_plans(self, gene):
        return {
            'num_floors': gene.children[0].value,
            'floor_height': gene.children[1].value
        }

    def decode_mep_systems(self, gene):
        return {
            'hvac_type': gene.children[0].value,
            'lighting_type': gene.children[1].value,
            'plumbing_type': gene.children[2].value,
            'renewable_energy': gene.children[3].value
        }

    def decode_facade(self, gene):
        return {
            'window_ratio': gene.children[0].value,
            'material': gene.children[1].value
        }

# Example use case
if __name__ == "__main__":
    from ..genetic_algorithm.encoding import BuildingGenome
    
    genome = BuildingGenome()
    decoder = Decoder()
    architectural_design = decoder.decode(genome)
    print(architectural_design)