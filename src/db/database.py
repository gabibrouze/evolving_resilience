# "src/db/database.py"

## The Database class provides the following functionality:
## - Creating and connecting to an SQLite database
## - Saving and retrieving building designs (genomes and their fitness scores)
## - Saving and retrieving optimisation history (generation-wise best and average fitness scores)

import sqlite3
import pickle
from datetime import datetime
import numpy as np

class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.check_and_update_schema()

    def create_tables(self):
        # Create buildings table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS buildings (
                id INTEGER PRIMARY KEY,
                genome BLOB,
                fitness_scores BLOB,
                overall_fitness REAL,
                creation_date TIMESTAMP
            )
        ''')

        # Create optimisation_history table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS optimisation_history (
                id INTEGER PRIMARY KEY,
                generation INTEGER,
                best_fitness BLOB,
                average_fitness BLOB,
                timestamp TIMESTAMP
            )
        ''')
        self.conn.commit()

    def check_and_update_schema(self):
        self.cursor.execute("PRAGMA table_info(buildings)")
        columns = [col[1] for col in self.cursor.fetchall()]
        
        if 'overall_fitness' not in columns:
            # print("Adding overall_fitness column to buildings table")
            self.cursor.execute("ALTER TABLE buildings ADD COLUMN overall_fitness REAL")
            self.conn.commit()
  

    def save_building(self, genome, fitness_scores):
        genome_blob = pickle.dumps(genome)
        fitness_blob = pickle.dumps(fitness_scores)
        
        # Calculate an overall fitness score (e.g., average of all objectives)
        overall_fitness = np.mean(fitness_scores)
        
        self.cursor.execute('''
            INSERT INTO buildings (genome, fitness_scores, overall_fitness, creation_date)
            VALUES (?, ?, ?, ?)
        ''', (genome_blob, fitness_blob, overall_fitness, datetime.now()))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_building(self, building_id):
        self.cursor.execute('SELECT * FROM buildings WHERE id = ?', (building_id,))
        row = self.cursor.fetchone()
        if row:
            return {
                'id': row[0],
                'genome': pickle.loads(row[1]),
                'fitness_scores': pickle.loads(row[2]),
                'overall_fitness': row[3],
                'creation_date': row[4]
            }
        return None

    def save_optimisation_history(self, generation, best_fitness, average_fitness):
        best_fitness_blob = pickle.dumps(best_fitness)
        average_fitness_blob = pickle.dumps(average_fitness)
        self.cursor.execute('''
            INSERT INTO optimisation_history (generation, best_fitness, average_fitness, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (generation, best_fitness_blob, average_fitness_blob, datetime.now()))
        self.conn.commit()

    def get_optimisation_history(self):
        self.cursor.execute('SELECT * FROM optimisation_history ORDER BY generation')
        history = []
        for row in self.cursor.fetchall():
            history.append({
                'generation': row[1],
                'best_fitness': pickle.loads(row[2]),
                'average_fitness': pickle.loads(row[3]),
                'timestamp': row[4]
            })
        return history

    def close(self):
        self.conn.close()

# Example use case
if __name__ == "__main__":
    db = Database("buildings.db")
    
    # Simulating genome and fitness scores
    class MockGenome:
        def __init__(self, data):
            self.data = data

    mock_genome = MockGenome({"height": 50, "width": 30, "length": 40})
    mock_fitness_scores = {"safety": 0.8, "energy_efficiency": 0.7, "cost": 0.6}

    # Save a building
    building_id = db.save_building(mock_genome, mock_fitness_scores)
    print(f"Saved building with ID: {building_id}")

    # Retrieve the building
    retrieved_building = db.get_building(building_id)
    print("Retrieved building:", retrieved_building)

    # Save optimisation history
    db.save_optimisation_history(1, {"safety": 0.85, "energy_efficiency": 0.75, "cost": 0.65}, 
                                 {"safety": 0.8, "energy_efficiency": 0.7, "cost": 0.6})

    # Get optimisation history
    history = db.get_optimisation_history()
    print("Optimisation history:", history)

    db.close()