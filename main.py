# This is the working main.py file. 

import bpy
import os
from mathutils import Vector

def clear_scene():
    # Delete all mesh objects
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    return

def import_glb():
    from bpy.types import Operator
    from bpy.props import StringProperty, BoolProperty
    from bpy_extras.io_utils import ImportHelper

    # Generates file browser pop-up window
    class OT_TestOpenFilebrowser(Operator, ImportHelper):
        bl_idname = "test.open_filebrowser"
        bl_label = "Open the file browser (yay)"
        
        filter_glob: StringProperty(
            default='*.glb',
            options={'HIDDEN'}
        )
        
        some_boolean: BoolProperty(
            name='Do a thing',
            description='Do a thing with the file you\'ve selected',
            default=True,
        )

        def execute(self, context):
            """Do something with the selected file(s)."""
            filename, extension = os.path.splitext(self.filepath)
            print('Selected file:', self.filepath)
            print('File name:', filename)
            print('File extension:', extension)
            print('Some Boolean:', self.some_boolean)
            
            # Import the selected file into Blender
            bpy.ops.import_scene.gltf(filepath=self.filepath)
            
            return {'FINISHED'}
    # Instantiate your file browser operation with arguments
    bpy.utils.register_class(OT_TestOpenFilebrowser)
    result = bpy.ops.test.open_filebrowser('INVOKE_DEFAULT')
    
    # Check if operation is finished
    if result == {'FINISHED'}:
        # Run the next step in your script
        print("File browser operation finished, running next step...")
    else:
        # Handle potential errors or other outcomes
        print("File browser operation failed or was canceled.")

    return

def SelectFace():
    return

def ManualAdjustment():
    return

def DrawRectangle():
    return

def GenerateClippedSurface():
    return

def Nurbs():
    return

def GenerateNurbsSolid():
    return

def AddThickness():
    return

def SmoothSurface():
    return
    
def GenerateBust():
    return

def GenerateNegative():
    return

def CutNurbs():
    return

def temp():


    # Import the .glb file
    bpy.ops.import_scene.gltf(filepath=file_path)

    # Get the imported object
    imported_object = bpy.context.selected_objects[0]

    # Calculate the dimensions of the imported object
    dimensions = imported_object.dimensions

    # Create a cube that is 2 times bigger than the imported object(This is done to ensure that the object is fully inside the cube. It is essential to do this. If the cube isnt big enough, there might be some problems) 
    bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(2*dimensions.x, 2*dimensions.y, 2*dimensions.z))

    # Get the cube object
    cube_object = bpy.context.object

    # Move the cube to the center of the imported object
    cube_object.location = imported_object.location

    # Perform a boolean intersection operation
    boolean_modifier = cube_object.modifiers.new(name="Boolean", type='BOOLEAN')
    boolean_modifier.object = imported_object
    boolean_modifier.operation = 'INTERSECT'
    boolean_modifier.solver = 'EXACT'

    # Apply the modifier
    bpy.ops.object.modifier_apply(modifier=boolean_modifier.name)

    #At this point the cube should be looking like the imported scan. Further modifications will be applied to the cube instead so make sure that the nameing is consistent 

    # Create a solidify modifier for the cube
    solidify_modifier = cube_object.modifiers.new(name="Solidify", type='SOLIDIFY')

    # Set the solidify settings
    solidify_modifier.thickness = 0.00477  # For 1/8' thickness. Change this to 0.00318 for 1/16' thickness.
    solidify_modifier.offset = 1.0
    solidify_modifier.use_even_offset = False
    solidify_modifier.use_rim = True
    solidify_modifier.use_rim_only = False

    # Apply the modifier
    bpy.ops.object.modifier_apply(modifier=solidify_modifier.name)

    # Create a smooth modifier for the cube: Smooth deform is used instead of laplace smoothing 
    smooth_modifier = cube_object.modifiers.new(name="Smooth", type='SMOOTH')

    # Set the smooth settings
    smooth_modifier.factor = 1.5
    smooth_modifier.iterations = 1

    # Apply the modifier
    bpy.ops.object.modifier_apply(modifier=smooth_modifier.name)


    #At this point, imported scan should be looking smooth and have some thickness. Adjust the smoothing factors if the scan is not smooth enough 
    #Further process from here is to generate the positive and negative mould 

    # Add a new cube  
    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0))
    cube_001 = bpy.context.object
    cube_001.name = "Cube.001"

    # Scale Cube.001 
    cube_001.scale = (0.05, 0.05, 0.05) #By default we are using the scale of 0.05 but this can be adjusted as per need.
    bpy.ops.object.transform_apply(scale=True)

    # Duplicate Cube.001 and name it Cube.002
    bpy.ops.object.duplicate(linked=False)
    cube_002 = bpy.context.object
    cube_002.name = "Cube.002"

    # Upscale Cube.001
    cube_001.scale = (1.000001, 1.000001, 1.000001)
    bpy.ops.object.transform_apply(scale=True)

    # Get the solidified and smoothed cube (Make sure the naming of meshes are consistent
    cube = bpy.data.objects['Cube']

    # Select Cube.001
    cube_001.select_set(True)
    bpy.context.view_layer.objects.active = cube_001

    # Create a boolean modifier for Cube.001
    boolean_modifier = cube_001.modifiers.new(name="Boolean", type='BOOLEAN')

    # Set the boolean settings
    boolean_modifier.operation = 'INTERSECT'
    boolean_modifier.object = cube
    boolean_modifier.solver = 'EXACT'

    # Apply the modifier
    bpy.ops.object.modifier_apply(modifier=boolean_modifier.name)

    # Select Cube.002
    bpy.data.objects['Cube.002'].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects['Cube.002']

    # Create a boolean modifier for Cube.002
    boolean_modifier = bpy.data.objects['Cube.002'].modifiers.new(name="Boolean", type='BOOLEAN')

    # Set the boolean settings
    boolean_modifier.operation = 'DIFFERENCE'
    boolean_modifier.object = bpy.data.objects['Cube.001']
    boolean_modifier.solver = 'EXACT'

    # Apply the modifier
    bpy.ops.object.modifier_apply(modifier=boolean_modifier.name)





# Run the code
clear_scene() #working
import_glb() #working
SelectFace() 
ManualAdjustment()
DrawRectangle()
GenerateClippedSurface()
Nurbs()
GenerateNurbsSolid()
AddThickness()
SmoothSurface()
SmoothSurface()
GenerateBust()
GenerateNegative()
CutNurbs()

