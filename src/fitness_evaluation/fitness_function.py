# "src/fitness_evaluation/fitness_function.py"

## The FitnessFunction class has the following responsibilities:
## 1. Evaluate the performance of a building design based on the genome
## 2. Update the weights of the fitness function
## 3. Calculate the total score of the building design
## 4. Provide the scores and weighted scores of the building design

import traceback
class FitnessFunction:
    def __init__(self, weights=None):
        if weights is None:
            weights = {
                'safety': 0.3,
                'structural': 0.3,
                'livability': 0.2,
                'energy': 0.1,
                'cost': 0.1
            }
        self.weights = weights

    def evaluate(self, genome, evaluate_genome_func):
        try:
            print("Starting genome evaluation")
            scores = evaluate_genome_func(genome)
            print(f"Raw scores: {scores}")

            scores = {
                'safety': (scores[0] + scores[5] + scores[6]) / 3,
                'structural': scores[1],
                'livability': scores[2],
                'energy': scores[3],
                'cost': scores[4]
            }
            print(f"Processed scores: {scores}")

            weighted_scores = {key: self.weights[key] * score for key, score in scores.items()}
            print(f"Weighted scores: {weighted_scores}")

            total_score = sum(weighted_scores.values())
            print(f"Total score: {total_score}")

            return scores, weighted_scores, total_score
        
        except Exception as e:
            print(f"Error in FitnessFunction.evaluate: {str(e)}")
            print(traceback.format_exc())
            return {}, {}, 0


    # def evaluate(self, genome, evaluate_genome_func):
    #     scores = evaluate_genome_func(genome)

    #     scores = {
    #         'safety': (scores[0] + scores[5] + scores[6]) / 3,  # Average of safety, pedestrian flow, and blast resistance
    #         'structural': scores[1],
    #         'livability': scores[2],
    #         'energy': scores[3],
    #         'cost': scores[4]
    #     }

    #     weighted_scores = {key: self.weights[key] * score for key, score in scores.items()}
    #     total_score = sum(weighted_scores.values())

    #     return scores, weighted_scores, total_score

    def update_weights(self, new_weights):
        self.weights.update(new_weights)

# Example use
if __name__ == "__main__":
    class MockGenome:
        def __init__(self, data):
            self.data = data

    def mock_evaluate_genome(genome):
        # Mock function to simulate genome evaluation
        return [0.8, 0.7, 0.9, 0.6, 0.5, 0.8, 0.7]  # safety, structural, livability, energy, cost, pedestrian, blast

    mock_genome = MockGenome({"height": 50, "width": 30, "length": 40})
    fitness_function = FitnessFunction()

    scores, weighted_scores, total_score = fitness_function.evaluate(mock_genome, mock_evaluate_genome)
    print("Scores:", scores)
    print("Weighted scores:", weighted_scores)
    print("Total score:", total_score)

    # Update weights
    fitness_function.update_weights({'safety': 0.2, 'cost': 0.2})
    scores, weighted_scores, total_score = fitness_function.evaluate(mock_genome, mock_evaluate_genome)
    print("\nAfter updating weights:")
    print("Scores:", scores)
    print("Weighted scores:", weighted_scores)
    print("Total score:", total_score)