# "src/visualisation/building_visualiser.py"

## The BuildingVisualiser class visualises the building design based on the genome of the building.

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

class BuildingVisualiser:
    def __init__(self, genome):
        self.genome = genome

    def visualise(self):
        # Extract building parameters
        height = self.genome.genes['building_envelope'].children[0].value
        width = self.genome.genes['building_envelope'].children[1].value
        length = self.genome.genes['building_envelope'].children[2].value
        shape = self.genome.genes['building_envelope'].children[3].value
        material = self.genome.genes['structural_system'].children[0].value
        num_floors = self.genome.genes['floor_plans'].children[0].value
        window_ratio = self.genome.genes['facade'].children[0].value

        # Create figure and 3D axis
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')

        # Generate building vertices based on shape
        if shape == 'rectangular':
            vertices = self._get_rectangular_vertices(width, length, height)
        elif shape == 'L-shaped':
            vertices = self._get_l_shaped_vertices(width, length, height)
        else:  # U-shaped
            vertices = self._get_u_shaped_vertices(width, length, height)

        # Create building faces
        faces = Poly3DCollection(vertices, alpha=0.5)

        # Set face colors based on material
        if material == 'concrete':
            faces.set_facecolor('gray')
        elif material == 'steel':
            faces.set_facecolor('silver')
        else:  # timber
            faces.set_facecolor('peru')

        # Add building to plot
        ax.add_collection3d(faces)

        # Add windows
        self._add_windows(ax, vertices, window_ratio, num_floors)

        # Set plot limits and labels
        max_dim = max(width, length, height)
        ax.set_xlim(0, max_dim)
        ax.set_ylim(0, max_dim)
        ax.set_zlim(0, max_dim)
        ax.set_xlabel('Width')
        ax.set_ylabel('Length')
        ax.set_zlabel('Height')

        # Set title with key building parameters
        plt.title(f"Building Design\nShape: {shape}, Material: {material}\n"
                  f"Dimensions: {width:.1f}x{length:.1f}x{height:.1f}, Floors: {num_floors}")

        plt.show()

    def _get_rectangular_vertices(self, width, length, height):
        # [bottom, top, front, back, left, right]
        return [
            [[0, 0, 0], [width, 0, 0], [width, length, 0], [0, length, 0]],  # bottom
            [[0, 0, height], [width, 0, height], [width, length, height], [0, length, height]],  # top
            [[0, 0, 0], [width, 0, 0], [width, 0, height], [0, 0, height]],  # front
            [[0, length, 0], [width, length, 0], [width, length, height], [0, length, height]],  # back
            [[0, 0, 0], [0, length, 0], [0, length, height], [0, 0, height]],  # left
            [[width, 0, 0], [width, length, 0], [width, length, height], [width, 0, height]]  # right
        ]

    def _get_l_shaped_vertices(self, width, length, height):
        w2, l2 = width/2, length/2
        # [bottom, top, front, back, inner back, left, right, inner right]
        return [
            [[0, 0, 0], [width, 0, 0], [width, l2, 0], [w2, l2, 0], [w2, length, 0], [0, length, 0]],  # bottom
            [[0, 0, height], [width, 0, height], [width, l2, height], [w2, l2, height], [w2, length, height], [0, length, height]],  # top
            [[0, 0, 0], [width, 0, 0], [width, 0, height], [0, 0, height]],  # front
            [[0, length, 0], [w2, length, 0], [w2, length, height], [0, length, height]],  # back
            [[w2, l2, 0], [width, l2, 0], [width, l2, height], [w2, l2, height]],  # inner back
            [[0, 0, 0], [0, length, 0], [0, length, height], [0, 0, height]],  # left
            [[width, 0, 0], [width, l2, 0], [width, l2, height], [width, 0, height]],  # right
            [[w2, l2, 0], [w2, length, 0], [w2, length, height], [w2, l2, height]]  # inner right
        ]

    def _get_u_shaped_vertices(self, width, length, height):
        w3, l3 = width/3, length/3
        # [bottom, top, front, left back, right back, inner back, left, right, inner left, inner right]
        return [
            [[0, 0, 0], [width, 0, 0], [width, l3, 0], [2*w3, l3, 0], [2*w3, 2*l3, 0], [w3, 2*l3, 0], [w3, l3, 0], [0, l3, 0]],  # bottom
            [[0, 0, height], [width, 0, height], [width, l3, height], [2*w3, l3, height], [2*w3, 2*l3, height], [w3, 2*l3, height], [w3, l3, height], [0, l3, height]],  # top
            [[0, 0, 0], [width, 0, 0], [width, 0, height], [0, 0, height]],  # front
            [[0, l3, 0], [w3, l3, 0], [w3, l3, height], [0, l3, height]],  # left back
            [[2*w3, l3, 0], [width, l3, 0], [width, l3, height], [2*w3, l3, height]],  # right back
            [[w3, 2*l3, 0], [2*w3, 2*l3, 0], [2*w3, 2*l3, height], [w3, 2*l3, height]],  # inner back
            [[0, 0, 0], [0, l3, 0], [0, l3, height], [0, 0, height]],  # left
            [[width, 0, 0], [width, l3, 0], [width, l3, height], [width, 0, height]],  # right
            [[w3, l3, 0], [w3, 2*l3, 0], [w3, 2*l3, height], [w3, l3, height]],  # inner left
            [[2*w3, l3, 0], [2*w3, 2*l3, 0], [2*w3, 2*l3, height], [2*w3, l3, height]]  # inner right
        ]

    def _add_windows(self, ax, vertices, window_ratio, num_floors):
        # Add windows to each face
        for face in vertices[2:]:  # Skip bottom and top faces
            for i in range(num_floors):
                floor_height = face[0][2] / num_floors
                z = i * floor_height
                window_height = floor_height * 0.6  # Window takes 60% of floor height
                window_start = z + (floor_height - window_height) / 2

                x_coords = [v[0] for v in face]
                y_coords = [v[1] for v in face]

                min_x, max_x = min(x_coords), max(x_coords)
                min_y, max_y = min(y_coords), max(y_coords)

                if max_x - min_x > 0.1:  # Vertical face
                    window_width = (max_x - min_x) * window_ratio
                    x_start = min_x + (max_x - min_x - window_width) / 2
                    ax.add_collection3d(Poly3DCollection([
                        [[x_start, min_y, window_start], [x_start + window_width, min_y, window_start],
                         [x_start + window_width, min_y, window_start + window_height], [x_start, min_y, window_start + window_height]]
                    ], facecolors='skyblue', edgecolors='black'))

                if max_y - min_y > 0.1:  # Horizontal face
                    window_width = (max_y - min_y) * window_ratio
                    y_start = min_y + (max_y - min_y - window_width) / 2
                    ax.add_collection3d(Poly3DCollection([
                        [[min_x, y_start, window_start], [min_x, y_start + window_width, window_start],
                         [min_x, y_start + window_width, window_start + window_height], [min_x, y_start, window_start + window_height]]
                    ], facecolors='skyblue', edgecolors='black'))

# Example use case
if __name__ == "__main__":
    from src.genetic_algorithm.encoding import BuildingGenome
    
    genome = BuildingGenome()
    visualiser = BuildingVisualiser(genome)
    visualiser.visualise()