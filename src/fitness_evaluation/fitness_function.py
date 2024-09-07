# "src/fitness_evaluation/fitness_function.py"

## The FitnessFunction class has the following responsibilities:
## 1. Evaluate the performance of a building design based on the genome
## 2. Update the weights of the fitness function
## 3. Calculate the total score of the building design
## 4. Provide the scores and weighted scores of the building design

from ..genetic_algorithm.evolution import EvolutionaryAlgorithm as ea

class FitnessFunction:
    def __init__(self, weights=None):
        if weights is None:
            weights = {
                'safety': 0.3,
                'structural': 0.3,
                'livability': 0.15,
                'energy': 0.1,
                'cost': 0.05,
                'pedestrian_flow': 0.05,
                'blast_resistance': 0.05
            }
        self.weights = weights

    def evaluate(self, genome):
        scores = ea.evaluate_genome(genome)

        scores = {
            'safety': scores[0],  
            'structural': scores[1],
            'livability': scores[2],
            'energy': scores[3],
            'cost': scores[4],
            'pedestrian_flow': scores[5],
            'blast_resistance': scores[6]
        }

        weighted_scores = {key: self.weights[key] * score for key, score in scores.items()}
        total_score = sum(weighted_scores.values())

        return scores, weighted_scores, total_score

    def update_weights(self, new_weights):
        self.weights.update(new_weights)

# Example use
if __name__ == "__main__":
    class MockGenome:
        def __init__(self, data):
            self.data = data

    # Mock the simulation engine functions for testing
    scores = {
        'safety': 0.8,
        'structural': 0.8,
        'livability': 0.8,
        'energy': 0.8,
        'cost': 0.8,
        'pedestrian_flow': 0.8,
        'blast_resistance': 0.8
    }

    mock_genome = MockGenome({"height": 50, "width": 30, "length": 40})
    fitness_function = FitnessFunction()

    scores, weighted_scores, total_score = fitness_function.evaluate(mock_genome)
    print("Scores:", scores)
    print("Weighted scores:", weighted_scores)
    print("Total score:", total_score)

    # Update weights
    fitness_function.update_weights({'safety': 0.2, 'cost': 0.2})
    scores, weighted_scores, total_score = fitness_function.evaluate(mock_genome)
    print("\nAfter updating weights:")
    print("Scores:", scores)
    print("Weighted scores:", weighted_scores)
    print("Total score:", total_score)