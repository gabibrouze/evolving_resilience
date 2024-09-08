# "src/bim_integration/ifc_interface.py"

## The IFCInterface class provides methods to:
## - import building designs from IFC files.
## - export building designs to IFC files.
## It uses the IfcOpenShell library to:
## - read and write IFC files 
## - extract building information.
## The class can be used to integrate the genetic algorithm with building information modelling (BIM) tools.

## sources:
## https://ifcopenshell.org/docs/

import ifcopenshell
import ifcopenshell.geom
import numpy as np
from ..genetic_algorithm.encoding import BuildingGenome

class IFCInterface:
    def __init__(self):
        self.settings = ifcopenshell.geom.settings()
        self.settings.set(self.settings.USE_WORLD_COORDS, True)

    def import_from_ifc(self, file_path):
        # 1. Load IFC file and extract building entity
        ifc_file = ifcopenshell.open(file_path)
        building = ifc_file.by_type("IfcBuilding")[0]

        # 2. Calculate building dimensions
        bbox = self.calculate_bounding_box(building)
        width = bbox[1][0] - bbox[0][0]
        length = bbox[1][1] - bbox[0][1]
        height = bbox[1][2] - bbox[0][2]

        # 3. Extract information (basic building properties, materials, windows, MEP, structural, ...)
        storeys = ifc_file.by_type("IfcBuildingStorey")
        num_floors = len(storeys)
        materials = self.get_building_materials(ifc_file)
        primary_material = max(materials, key=materials.count) if materials else "concrete"
        window_ratio = self.calculate_window_ratio(ifc_file)
        hvac_type = self.get_hvac_type(ifc_file)
        has_renewable_energy = self.check_renewable_energy(ifc_file)
        frame_type = self.get_frame_type(ifc_file)
        shape = self.determine_building_shape(bbox)
 
        # 4. Create, populate and return genome
        genome = BuildingGenome()
        genome.genes['building_envelope'].children[0].value = height
        genome.genes['building_envelope'].children[1].value = width
        genome.genes['building_envelope'].children[2].value = length
        genome.genes['building_envelope'].children[3].value = shape
        genome.genes['structural_system'].children[0].value = primary_material
        genome.genes['structural_system'].children[1].value = frame_type
        genome.genes['floor_plans'].children[0].value = num_floors
        genome.genes['floor_plans'].children[1].value = height / num_floors  # Approximate floor height
        genome.genes['mep_systems'].children[0].value = hvac_type
        genome.genes['mep_systems'].children[3].value = has_renewable_energy
        genome.genes['facade'].children[0].value = window_ratio
        return genome

    def export_to_ifc(self, genome, file_path):
        ifc_file = ifcopenshell.file()

        # 1. Create IFC entities
        project = ifc_file.createIfcProject("Project")
        site = ifc_file.createIfcSite("Site")
        building = ifc_file.createIfcBuilding("Building")

        # 2. Extract genome properties
        height = genome.genes['building_envelope'].children[0].value
        width = genome.genes['building_envelope'].children[1].value
        length = genome.genes['building_envelope'].children[2].value
        material = genome.genes['structural_system'].children[0].value
        num_floors = genome.genes['floor_plans'].children[0].value

        # 3. Create building storeys
        for i in range(num_floors):
            storey = ifc_file.createIfcBuildingStorey(f"Floor {i+1}")
            ifc_file.createIfcRelAggregates(f"BuildingToStorey{i+1}", building, [storey])

        # 4. Create a simple box representation for the building
        box = ifc_file.createIfcBoundingBox(
            ifcopenshell.createIfcCartesianPoint(ifc_file, (0., 0., 0.)),
            width, length, height
        )
        building_shape = ifc_file.createIfcShapeRepresentation(
            ifc_file.by_type("IfcGeometricRepresentationContext")[0],
            "Body", "BoundingBox", [box]
        )
        ifc_file.createIfcProductDefinitionShape(Representations=[building_shape])

        # 5. Assign material
        material_def = ifc_file.createIfcMaterial(material)
        ifc_file.createIfcRelAssociatesMaterial(f"BuildingMaterial", RelatedObjects=[building], RelatingMaterial=material_def)

        # 6. Add export functionality here
        self.add_windows(ifc_file, building, genome.genes['facade'].children[0].value)
        self.add_mep_systems(ifc_file, building, genome.genes['mep_systems'])
        self.add_structural_elements(ifc_file, building, genome.genes['structural_system'])

        # 7. Save IFC file
        ifc_file.write(file_path)

    def calculate_bounding_box(self, product):
        bbox_min = np.array([float('inf'), float('inf'), float('inf')])
        bbox_max = np.array([float('-inf'), float('-inf'), float('-inf')])

        if product.is_a("IfcProduct"):
            try:
                shape = ifcopenshell.geom.create_shape(self.settings, product)
                verts = shape.verts
                for i in range(0, len(verts), 3):
                    point = np.array(verts[i:i+3])
                    bbox_min = np.minimum(bbox_min, point)
                    bbox_max = np.maximum(bbox_max, point)
            except RuntimeError:
                pass

        return (bbox_min, bbox_max)

    def get_element_material(self, element):
        if element.HasAssociations:
            for association in element.HasAssociations:
                if association.is_a("IfcRelAssociatesMaterial"):
                    material = association.RelatingMaterial
                    if material.is_a("IfcMaterial"):
                        return material.Name
        return None
    
    def get_building_materials(self, ifc_file):
        materials = []
        for element in ifc_file.by_type("IfcElement"):
            material = self.get_element_material(element)
            if material:
                materials.append(material)
        return materials
    
    def calculate_window_ratio(self, ifc_file):
        total_wall_area = 0
        total_window_area = 0
        for wall in ifc_file.by_type("IfcWall"):
            wall_shape = ifcopenshell.geom.create_shape(self.settings, wall)
            total_wall_area += wall_shape.area
        for window in ifc_file.by_type("IfcWindow"):
            window_shape = ifcopenshell.geom.create_shape(self.settings, window)
            total_window_area += window_shape.area
        return total_window_area / total_wall_area if total_wall_area > 0 else 0

    def get_hvac_type(self, ifc_file):
        hvac_systems = ifc_file.by_type("IfcSystem")
        # TODO: Implement more detailed logic to determine the HVAC type
        if any("central" in system.Name.lower() for system in hvac_systems):
            return "central"
        elif any("distributed" in system.Name.lower() for system in hvac_systems):
            return "distributed"
        else:
            return "hybrid"
        
    def check_renewable_energy(self, ifc_file):
        energy_systems = ifc_file.by_type("IfcEnergyConversionDevice")
        return any("solar" in system.Name.lower() or "wind" in system.Name.lower() for system in energy_systems)

    def determine_building_shape(self, bbox):
        width = bbox[1][0] - bbox[0][0]
        length = bbox[1][1] - bbox[0][1]
        if abs(width - length) < 0.1 * max(width, length):
            return "rectangular"
        elif min(width, length) < 0.5 * max(width, length):
            return "L-shaped"
        else:
            return "U-shaped"
        
    def get_frame_type(self, ifc_file):
        structural_elements = ifc_file.by_type("IfcStructuralMember")
        frame_types = [elem.PredefinedType for elem in structural_elements if hasattr(elem, 'PredefinedType')]
        if "BEAM" in frame_types and "COLUMN" in frame_types:
            return "moment frame"
        elif "BRACE" in frame_types:
            return "braced frame"
        elif "WALL" in frame_types:
            return "shear wall"
        else:
            return "moment frame"  # Default if unable to determine

    def add_windows(self, ifc_file, building, window_ratio):
        # TODO: Implement more complex window addition logic
        for wall in ifc_file.by_type("IfcWall"):
            wall_shape = ifcopenshell.geom.create_shape(self.settings, wall)
            window_area = wall_shape.area * window_ratio
            window = ifc_file.createIfcWindow(
                ifcopenshell.guid.new(),
                self.owner_history,
                "Window",
                "Generated Window",
                None,
                None,
                None,
                None,
                window_area
            )
            ifc_file.createIfcRelFillsElement(ifcopenshell.guid.new(), self.owner_history, None, None, wall, window)

    def add_mep_systems(self, ifc_file, building, mep_genes):
        hvac_type = mep_genes.children[0].value
        has_renewable = mep_genes.children[3].value
        
        hvac_system = ifc_file.createIfcSystem(
            ifcopenshell.guid.new(),
            self.owner_history,
            f"{hvac_type.capitalize()} HVAC System",
            "HVAC",
            None
        )
        
        if has_renewable:
            renewable_system = ifc_file.createIfcSystem(
                ifcopenshell.guid.new(),
                self.owner_history,
                "Renewable Energy System",
                "ENERGY",
                None
            )
            solar_panel = ifc_file.createIfcEnergyConversionDevice(
                ifcopenshell.guid.new(),
                self.owner_history,
                "Solar Panel",
                None,
                None,
                None,
                None,
                "SOLARPANEL"
            )
            ifc_file.createIfcRelAssignsToGroup(ifcopenshell.guid.new(), self.owner_history, None, None, [solar_panel], None, renewable_system)

        ifc_file.createIfcRelContainedInSpatialStructure(ifcopenshell.guid.new(), self.owner_history, None, None, [hvac_system, renewable_system] if has_renewable else [hvac_system], building)

    def add_structural_elements(self, ifc_file, building, structural_genes):
        material = structural_genes.children[0].value
        frame_type = structural_genes.children[1].value
        
        material_def = ifc_file.createIfcMaterial(material)
        
        if frame_type == "moment frame":
            self.add_moment_frame(ifc_file, building, material_def)
        elif frame_type == "braced frame":
            self.add_braced_frame(ifc_file, building, material_def)
        elif frame_type == "shear wall":
            self.add_shear_wall(ifc_file, building, material_def)

        ifc_file.createIfcRelAggregates(ifcopenshell.guid.new(), None, "StructuralElements", None, [building])

    def add_moment_frame(self, ifc_file, building, material):
        # Simple moment frame creation
        for i in range(3):  # Create 3 columns and 2 beams as an example
            column = ifc_file.createIfcColumn(
                ifcopenshell.guid.new(),
                self.owner_history,
                f"Column {i+1}",
                None,
                None,
                None,
                None,
                None
            )
            ifc_file.createIfcRelAssociatesMaterial(ifcopenshell.guid.new(), self.owner_history, None, None, [column], material)
            
            if i < 2:
                beam = ifc_file.createIfcBeam(
                    ifcopenshell.guid.new(),
                    self.owner_history,
                    f"Beam {i+1}",
                    None,
                    None,
                    None,
                    None,
                    None
                )
                ifc_file.createIfcRelAssociatesMaterial(ifcopenshell.guid.new(), self.owner_history, None, None, [beam], material)

        ifc_file.createIfcRelContainedInSpatialStructure(ifcopenshell.guid.new(), self.owner_history, None, None, [column, beam], building)

    def add_braced_frame(self, ifc_file, building, material):
        # Create a simple braced frame
        column_height = building.ObjectPlacement.RelativePlacement.Location.Coordinates[2]
        bay_width = 5.0  # Assume a 5-meter bay width
        
        # Create two columns
        column1 = ifc_file.createIfcColumn(
            ifcopenshell.guid.new(),
            self.owner_history,
            "Column 1",
            None,
            None,
            self.create_placement(ifc_file, 0, 0, 0),
            self.create_extruded_area_solid(ifc_file, 0.3, 0.3, column_height),
            None
        )
        
        column2 = ifc_file.createIfcColumn(
            ifcopenshell.guid.new(),
            self.owner_history,
            "Column 2",
            None,
            None,
            self.create_placement(ifc_file, bay_width, 0, 0),
            self.create_extruded_area_solid(ifc_file, 0.3, 0.3, column_height),
            None
        )
        
        # Create a beam
        beam = ifc_file.createIfcBeam(
            ifcopenshell.guid.new(),
            self.owner_history,
            "Beam",
            None,
            None,
            self.create_placement(ifc_file, 0, 0, column_height),
            self.create_extruded_area_solid(ifc_file, bay_width, 0.3, 0.5),
            None
        )
        
        # Create a brace
        brace = ifc_file.createIfcMember(
            ifcopenshell.guid.new(),
            self.owner_history,
            "Brace",
            None,
            None,
            self.create_placement(ifc_file, 0, 0, 0),
            self.create_extruded_area_solid(ifc_file, np.sqrt(bay_width**2 + column_height**2), 0.2, 0.2),
            None,
            "BRACE"
        )
        
        # Assign material to elements
        for element in [column1, column2, beam, brace]:
            ifc_file.createIfcRelAssociatesMaterial(ifcopenshell.guid.new(), self.owner_history, None, None, [element], material)
        
        # Add elements to the building
        ifc_file.createIfcRelContainedInSpatialStructure(ifcopenshell.guid.new(), self.owner_history, None, None, [column1, column2, beam, brace], building)
    
    def add_shear_wall(self, ifc_file, building, material):
        # Create a simple shear wall
        wall_height = building.ObjectPlacement.RelativePlacement.Location.Coordinates[2]
        wall_width = 5.0  # Assume a 5-meter wide wall
        wall_thickness = 0.3  # 30 cm thick wall
        
        # Create the wall
        wall = ifc_file.createIfcWall(
            ifcopenshell.guid.new(),
            self.owner_history,
            "Shear Wall",
            None,
            None,
            self.create_placement(ifc_file, 0, 0, 0),
            self.create_extruded_area_solid(ifc_file, wall_width, wall_thickness, wall_height),
            None,
            "SHEAR"
        )
        
        # Assign material to the wall
        ifc_file.createIfcRelAssociatesMaterial(ifcopenshell.guid.new(), self.owner_history, None, None, [wall], material)
        
        # Add the wall to the building
        ifc_file.createIfcRelContainedInSpatialStructure(ifcopenshell.guid.new(), self.owner_history, None, None, [wall], building)

    def create_placement(self, ifc_file, x, y, z):
        point = ifc_file.createIfcCartesianPoint((x, y, z))
        axis = ifc_file.createIfcDirection((0., 0., 1.))
        ref_direction = ifc_file.createIfcDirection((1., 0., 0.))
        return ifc_file.createIfcLocalPlacement(None, ifc_file.createIfcAxis2Placement3D(point, axis, ref_direction))

    def create_extruded_area_solid(self, ifc_file, x_dim, y_dim, height):
        point_list = [
            ifc_file.createIfcCartesianPoint((0., 0.)),
            ifc_file.createIfcCartesianPoint((x_dim, 0.)),
            ifc_file.createIfcCartesianPoint((x_dim, y_dim)),
            ifc_file.createIfcCartesianPoint((0., y_dim)),
            ifc_file.createIfcCartesianPoint((0., 0.))
        ]
        
        polyline = ifc_file.createIfcPolyline(point_list)
        closed_profile = ifc_file.createIfcArbitraryClosedProfileDef("AREA", None, polyline)
        
        direction = ifc_file.createIfcDirection((0., 0., 1.))
        extruded_area = ifc_file.createIfcExtrudedAreaSolid(closed_profile, None, direction, height)
        
        return extruded_area
    
# Example use case
if __name__ == "__main__":
    ifc_interface = IFCInterface()

    # Import from IFC
    imported_genome = ifc_interface.import_from_ifc("src/bim_integration/bim_import.ifc")
    print("Imported Genome:", imported_genome)
    
    # Export to IFC
    ifc_interface.export_to_ifc(imported_genome, "src/bim_integration/bim_export.ifc")
    print("Exported to IFC file")