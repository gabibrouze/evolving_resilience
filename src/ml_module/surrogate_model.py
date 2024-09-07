# "src/ml_module/surrogate_model.py"

## The SurrogateModel class provides the following functionality:
## - Training surrogate models for each objective using Random Forest Regressors.
## - Predicting fitness scores for new building designs.
## - Analysing feature importance to understand which building characteristics have the most impact on each objective.
## - Calculating permutation importance as a measure of feature importance.

import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from sklearn.inspection import permutation_importance

class SurrogateModel:
    def __init__(self, n_estimators=100):
        self.models = {}
        self.scalers = {}
        self.n_estimators = n_estimators
        self.objectives = ['structural_integrity', 'energy_efficiency', 'safety', 'livability', 'cost', 'pedestrian_flow', 'blast_resistance']
        self.is_trained = False

    def _genome_to_features(self, genome):
        features = [
            genome.genes['building_envelope'].children[0].value,  # height
            genome.genes['building_envelope'].children[1].value,  # width
            genome.genes['building_envelope'].children[2].value,  # length
            ['rectangular', 'L-shaped', 'U-shaped'].index(genome.genes['building_envelope'].children[3].value),  # shape
            ['concrete', 'steel', 'wood'].index(genome.genes['structural_system'].children[0].value),  # material
            ['moment frame', 'braced frame', 'shear wall'].index(genome.genes['structural_system'].children[1].value),  # frame_type
            genome.genes['floor_plans'].children[0].value,  # num_floors
            genome.genes['floor_plans'].children[1].value,  # floor_height
            ['central', 'distributed', 'hybrid'].index(genome.genes['mep_systems'].children[0].value),  # hvac_type
            int(genome.genes['mep_systems'].children[3].value),  # renewable_energy
            genome.genes['facade'].children[0].value,  # window_ratio
        ]
        return np.array(features).reshape(1, -1)

    def train(self, genomes, fitness_scores):
        X = np.array([self._genome_to_features(genome) for genome in genomes]).reshape(len(genomes), -1)
        
        for i, objective in enumerate(self.objectives):
            y = np.array([score[i] for score in fitness_scores])
            
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            model = RandomForestRegressor(n_estimators=self.n_estimators, random_state=42)
            model.fit(X_train_scaled, y_train)
            
            self.models[objective] = model
            self.scalers[objective] = scaler
            
            train_predictions = model.predict(X_train_scaled)
            test_predictions = model.predict(X_test_scaled)
            
            train_mse = mean_squared_error(y_train, train_predictions)
            test_mse = mean_squared_error(y_test, test_predictions)
            
            print(f"Surrogate Model for {objective} - Train MSE: {train_mse:.4f}, Test MSE: {test_mse:.4f}")
        
        self.is_trained = True

    def predict(self, genome):
        if not self.is_trained:
            raise ValueError("Surrogate model has not been trained yet.")
        
        features = self._genome_to_features(genome)
        predictions = {}
        
        for objective in self.objectives:
            features_scaled = self.scalers[objective].transform(features)
            predictions[objective] = self.models[objective].predict(features_scaled)[0]
        
        return predictions

    def feature_importance(self):
        if not self.is_trained:
            raise ValueError("Surrogate model has not been trained yet.")
        
        feature_names = [
            'height', 'width', 'length', 'shape', 'material', 'frame_type',
            'num_floors', 'floor_height', 'hvac_type', 'renewable_energy', 'window_ratio'
        ]
        
        importance_dict = {}
        
        for objective in self.objectives:
            importance = self.models[objective].feature_importances_
            importance_dict[objective] = dict(zip(feature_names, importance))
        
        return importance_dict

    def permutation_importance(self, X, y):
        if not self.is_trained:
            raise ValueError("Surrogate model has not been trained yet.")
        
        feature_names = [
            'height', 'width', 'length', 'shape', 'material', 'frame_type',
            'num_floors', 'floor_height', 'hvac_type', 'renewable_energy', 'window_ratio'
        ]
        
        perm_importance_dict = {}
        
        for objective in self.objectives:
            X_scaled = self.scalers[objective].transform(X)
            perm_importance = permutation_importance(self.models[objective], X_scaled, y[objective], n_repeats=10, random_state=42)
            perm_importance_dict[objective] = dict(zip(feature_names, perm_importance.importances_mean))
        
        return perm_importance_dict

# Example use case
if __name__ == "__main__":
    from src.genetic_algorithm.encoding import BuildingGenome
    from src.genetic_algorithm.evolution import EvolutionaryAlgorithm
    
    # Generate example data
    ea = EvolutionaryAlgorithm(population_size=100)
    genomes = ea.population
    fitness_scores = ea.evaluate_fitness()

    # Train the surrogate model
    surrogate = SurrogateModel()
    surrogate.train(genomes, fitness_scores)

    # Test the surrogate model
    test_genome = BuildingGenome()
    predicted_fitness = surrogate.predict(test_genome)
    print("Predicted fitness for test genome:")
    for objective, score in predicted_fitness.items():
        print(f"{objective}: {score:.4f}")

    # Analyse feature importance
    importance = surrogate.feature_importance()
    for objective, imp in importance.items():
        print(f"\nFeature importance for {objective}:")
        for feature, score in sorted(imp.items(), key=lambda x: x[1], reverse=True):
            print(f"{feature}: {score:.4f}")