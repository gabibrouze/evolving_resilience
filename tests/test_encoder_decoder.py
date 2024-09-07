# "tests/test_encoder_decoder.py"

import unittest
from src.encoder_decoder.encoder import Encoder
from src.encoder_decoder.decoder import Decoder
from src.genetic_algorithm.encoding import BuildingGenome

class TestEncoderDecoder(unittest.TestCase):
    def setUp(self):
        self.encoder = Encoder()
        self.decoder = Decoder()
        self.architectural_design = {
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

    def test_encode(self):
        genome = self.encoder.encode(self.architectural_design)
        self.assertIsInstance(genome, BuildingGenome)
        self.assertEqual(genome.genes['building_envelope'].children[0].value, 30)
        self.assertEqual(genome.genes['structural_system'].children[0].value, 'concrete')

    def test_decode(self):
        genome = self.encoder.encode(self.architectural_design)
        decoded_design = self.decoder.decode(genome)
        self.assertEqual(decoded_design['building_envelope']['height'], 30)
        self.assertEqual(decoded_design['structural_system']['material'], 'concrete')

    def test_encode_decode_consistency(self):
        genome = self.encoder.encode(self.architectural_design)
        decoded_design = self.decoder.decode(genome)
        self.assertEqual(self.architectural_design, decoded_design)

if __name__ == '__main__':
    unittest.main()