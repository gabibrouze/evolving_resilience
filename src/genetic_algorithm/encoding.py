# "src/genetic_algorithm/encoding.py"
## Defines the structure of the `BuildingGenome`,  including:
## - the `HierarchicalGene` structure
## - methods for mutation and crossover.
import numpy as np

class HierarchicalGene:
    def __init__(self, name, value, children=None):
        self.name = name
        self.value = value
        self.children = children or []
    
    def mutate(self, mutation_rate):
        if np.random.random() < mutation_rate:
            if isinstance(self.value, (int, float)):
                self.value *= np.random.uniform(0.8, 1.2)
            elif isinstance(self.value, str):
                pass
            elif isinstance(self.value, bool):
                self.value = not self.value

        for child in self.children:
            child.mutate(mutation_rate)

class BuildingGenome:
    def __init__(self):
        self.genes = {
            'building_envelope': HierarchicalGene('building_envelope', None, [
                HierarchicalGene('height', np.random.uniform(10, 100)),
                HierarchicalGene('width', np.random.uniform(10, 50)),
                HierarchicalGene('length', np.random.uniform(10, 50)),
                HierarchicalGene('shape', np.random.choice(['rectangular', 'L-shaped', 'U-shaped'])),
            ]),
            'structural_system': HierarchicalGene('structural_system', None, [
                HierarchicalGene('material', np.random.choice(['concrete', 'steel', 'wood'])),
                HierarchicalGene('frame_type', np.random.choice(['moment frame', 'braced frame', 'shear wall'])),
            ]),
            'floor_plans': HierarchicalGene('floor_plans', None, [
                HierarchicalGene('num_floors', np.random.randint(1, 20)),
                HierarchicalGene('floor_height', np.random.uniform(2.5, 4)),
            ]),
            'mep_systems': HierarchicalGene('mep_systems', None, [
                HierarchicalGene('hvac_type', np.random.choice(['central', 'distributed', 'hybrid'])),
                HierarchicalGene('lighting_type', np.random.choice(['LED', 'fluorescent', 'incandescent'])),
                HierarchicalGene('plumbing_type', np.random.choice(['central', 'distributed'])),
                HierarchicalGene('renewable_energy', np.random.choice([True, False])),
            ]),
            'facade': HierarchicalGene('facade', None, [
                HierarchicalGene('window_ratio', np.random.uniform(0.1, 0.6)),
                HierarchicalGene('material', np.random.choice(['glass', 'metal', 'composite'])),
            ]),
        }
    
    def mutate(self, mutation_rate=0.1):
        for gene in self.genes.values():
            gene.mutate(mutation_rate)

    def crossover(self, other):
        child = BuildingGenome()
        for key, gene in self.genes.items():
            if np.random.random() < 0.5:
                child.genes[key] = self._deep_copy_gene(gene)
            else:
                child.genes[key] = self._deep_copy_gene(other.genes[key])
        return child
    
    def _deep_copy_gene(self, gene):
        new_children = [self._deep_copy_gene(child) for child in gene.children]
        return HierarchicalGene(gene.name, gene.value, new_children)

    def __str__(self):
        return self._gene_to_string(self.genes)

    def _gene_to_string(self, gene, indent=0):
        if isinstance(gene, dict):
            return '\n'.join(f"{' ' * indent}{key}: {self._gene_to_string(value, indent + 2)}" for key, value in gene.items())
        elif isinstance(gene, HierarchicalGene):
            result = f"{gene.name}: {gene.value}"
            if gene.children:
                result += '\n' + '\n'.join(self._gene_to_string(child, indent + 2) for child in gene.children)
            return result
        else:
            return str(gene)

# Test the encoding
if __name__ == "__main__":
    genome1 = BuildingGenome()
    genome2 = BuildingGenome()
    
    print("Genome 1:")
    print(genome1)
    
    print("\nGenome 2:")
    print(genome2)
    
    child = genome1.crossover(genome2)
    print("\nChild Genome:")
    print(child)
    
    child.mutate()
    print("\nMutated Child Genome:")
    print(child)