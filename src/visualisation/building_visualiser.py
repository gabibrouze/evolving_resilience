# "src/visualisation/building_visualiser.py"

## The BuildingVisualiser class visualises the building design based on the genome of the building.

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

class BuildingVisualiser:
    def __init__(self, genome):
        self.genome = genome

    def visualise(self, ax):
        # Extract building parameters
        height = self.genome.genes['building_envelope'].children[0].value
        width = self.genome.genes['building_envelope'].children[1].value
        length = self.genome.genes['building_envelope'].children[2].value
        shape = self.genome.genes['building_envelope'].children[3].value
        material = self.genome.genes['structural_system'].children[0].value
        frame_type = self.genome.genes['structural_system'].children[1].value
        num_floors = self.genome.genes['floor_plans'].children[0].value
        window_ratio = self.genome.genes['facade'].children[0].value

        # Generate building vertices based on shape
        vertices = self._get_vertices(width, length, height, shape)

        # Create building faces
        faces = Poly3DCollection(vertices, linewidths=1, edgecolors='black')
         
        # Set face colours based on material
        colours = {'concrete': '#C0C0C0', 'steel': '#A8A8A8', 'wood': '#DEB887'}
        face_colour = colours.get(material, '#FF0000')
        faces.set_facecolor(face_colour)
        faces.set_alpha(0.6)  

        # Add building to plot
        ax.add_collection3d(faces)

        # Add structural elements
        self._add_structural_elements(ax, width, length, height, frame_type, num_floors)

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
        ax.set_title(f"Building Design\nShape: {shape}, Material: {material}, Frame: {frame_type}\n"
                     f"Dimensions: {width:.1f}x{length:.1f}x{height:.1f}, Floors: {num_floors}")
        
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
    
    def _get_vertices(self, width, length, height, shape):
        print(f"Shape: {shape}")
        if shape == 'rectangular':
            return self._get_rectangular_vertices(width, length, height)
        elif shape == 'L-shaped':
            return self._get_l_shaped_vertices(width, length, height)
        else:  # U-shaped
            return self._get_u_shaped_vertices(width, length, height)
    
    def _add_structural_elements(self, ax, width, length, height, frame_type, num_floors):
        if frame_type == 'moment frame':
            self._add_moment_frame(ax, width, length, height, num_floors)
        elif frame_type == 'braced frame':
            self._add_braced_frame(ax, width, length, height, num_floors)
        else:  # shear wall
            self._add_shear_wall(ax, width, length, height, num_floors)

    def _add_moment_frame(self, ax, width, length, height, num_floors):
        for i in range(num_floors + 1):
            z = i * height / num_floors
            ax.plot([0, width], [0, 0], [z, z], color='red', linewidth=2)
            ax.plot([0, width], [length, length], [z, z], color='red', linewidth=2)
            ax.plot([0, 0], [0, length], [z, z], color='red', linewidth=2)
            ax.plot([width, width], [0, length], [z, z], color='red', linewidth=2)

        for x in [0, width]:
            for y in [0, length]:
                ax.plot([x, x], [y, y], [0, height], color='red', linewidth=2)

    def _add_braced_frame(self, ax, width, length, height, num_floors):
        self._add_moment_frame(ax, width, length, height, num_floors)
        for i in range(num_floors):
            z1 = i * height / num_floors
            z2 = (i + 1) * height / num_floors
            ax.plot([0, width], [0, 0], [z1, z2], color='blue', linewidth=2)
            ax.plot([width, 0], [0, 0], [z1, z2], color='blue', linewidth=2)
            ax.plot([0, width], [length, length], [z1, z2], color='blue', linewidth=2)
            ax.plot([width, 0], [length, length], [z1, z2], color='blue', linewidth=2)

    def _add_shear_wall(self, ax, width, length, height, num_floors):
        wall_thickness = 0.3  # Assume 30cm thick walls
        wall_color = '#90EE90'  # Light green colour for shear walls
        
        # Left wall
        self._add_wall(ax, [0, 0, 0], [wall_thickness, length, height], wall_color)
        
        # Front wall
        self._add_wall(ax, [0, 0, 0], [width, wall_thickness, height], wall_color)
        
        # Right wall
        self._add_wall(ax, [width - wall_thickness, 0, 0], [width, length, height], wall_color)
        
        # Back wall
        self._add_wall(ax, [0, length - wall_thickness, 0], [width, length, height], wall_color)


    def _add_wall(self, ax, start, end, colour):
        x = [start[0], end[0], end[0], start[0], start[0]]
        y = [start[1], start[1], end[1], end[1], start[1]]
        z = [start[2], start[2], end[2], end[2], start[2]]
        verts = [list(zip(x, y, z))]
        ax.add_collection3d(Poly3DCollection(verts, facecolors=colour, edgecolors='black', alpha=0.7))

    def _add_windows(self, ax, vertices, window_ratio, num_floors):
        # Extract the total height of the building
        total_height = max(vertex[2] for face in vertices for vertex in face)
        floor_height = total_height / num_floors

        # Add windows to each face
        for face in vertices[2:]:  # Skip bottom and top faces
            for i in range(num_floors):
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
                    ], facecolors='skyblue', linewidths=1, edgecolors='blue'))

                if max_y - min_y > 0.1:  # Horizontal face
                    window_width = (max_y - min_y) * window_ratio
                    y_start = min_y + (max_y - min_y - window_width) / 2
                    ax.add_collection3d(Poly3DCollection([
                        [[min_x, y_start, window_start], [min_x, y_start + window_width, window_start],
                        [min_x, y_start + window_width, window_start + window_height], [min_x, y_start, window_start + window_height]]
                    ], facecolors='skyblue', linewidths=1, edgecolors='blue'))

# Example use case
if __name__ == "__main__":
    from src.genetic_algorithm.encoding import BuildingGenome
    import matplotlib.pyplot as plt
    
    genome = BuildingGenome()
    visualiser = BuildingVisualiser(genome)
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    visualiser.visualise(ax)
    plt.show()