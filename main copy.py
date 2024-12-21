# This is the working main.py file. 

import bpy
import os
import mathutils
import time
import numpy as np
from mathutils import Vector
from bpy.types import Operator
from bpy.props import StringProperty, BoolProperty
from bpy_extras.io_utils import ImportHelper

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
            
            #Note for future use: currently if you want the filebrowser method to work, you will need to run all the 
            #commands for the entire project within execute. So, selectFace() DrawRectangle() etc will need to be here. 

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

def SelectMesh():
    # Get the imported object
    imported_object = bpy.context.selected_objects[0]
    return imported_object

def DrawRectangle(imported_object):
    # Calculate the dimensions of the imported object
    dimensions = imported_object.dimensions

    # Create a cube that is 2 times bigger than the imported object(This is done to ensure that the object is fully inside the cube. It is essential to do this. If the cube isnt big enough, there might be some problems) 
    bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(2*dimensions.x, 2*dimensions.y, 2*dimensions.z))

    return

def GenerateBust(imported_object):
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

    return

def AddThickness(imported_object):
    #Get the cube object
    cube_object = bpy.context.object

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
   
    return

def SmoothSurface(imported_object):
    #Get the cube object
    cube_object = bpy.context.object

    # Create a smooth modifier for the cube: Smooth deform is used instead of laplace smoothing 
    smooth_modifier = cube_object.modifiers.new(name="Smooth", type='SMOOTH')

    # Set the smooth settings
    smooth_modifier.factor = 1.5
    smooth_modifier.iterations = 1

    # Apply the modifier
    bpy.ops.object.modifier_apply(modifier=smooth_modifier.name)


    #At this point, imported scan should be looking smooth and have some thickness. Adjust the smoothing factors if the scan is not smooth enough 
    #Further process from here is to generate the positive and negative mould 

    return
    
def OrientFace():

    # Function to calculate the best-fit plane from points
    def best_fit_plane(points):
        # Calculate centroid
        centroid = np.mean(points, axis=0)

        # Convert centroid to Vector
        centroid = Vector(centroid)

        return centroid

    # Get the active mesh object and its mesh data
    obj = bpy.context.active_object
    mesh = obj.data

    # Ensure we are in Object Mode
    bpy.ops.object.mode_set(mode='OBJECT')

    # Retrieve selected faces
    selected_faces = [f for f in mesh.polygons if f.select]

    # Check if any faces are selected
    if selected_faces:
        # Get the normal of the first selected face (assuming only one face is selected)
        normal = selected_faces[0].normal

        # Calculate the rotation quaternion to align the normal with the positive y-direction
        align_quaternion = normal.rotation_difference(Vector((0, 0, 1)))

        # Rotate the object
        obj.rotation_mode = 'QUATERNION'
        obj.rotation_quaternion = align_quaternion @ obj.rotation_quaternion
        
        # Make sure the object is in Object Mode
        bpy.ops.object.mode_set(mode='OBJECT')

        # Select the object
        obj.select_set(True)

        # Switch to Edit Mode
        bpy.ops.object.mode_set(mode='EDIT')

        # Get the vertices of the first selected face
        selected_verts_indices = selected_faces[0].vertices[:]
        selected_verts = [mesh.vertices[i].co for i in selected_verts_indices]

        # Convert selected vertices to numpy array
        selected_points = np.array(selected_verts)

        # Calculate the best-fit plane centroid
        centroid = best_fit_plane(selected_points)

        # Translate the object to make the centroid at the origin
        obj.location -= obj.matrix_world @ centroid

    else:
        print("No faces selected. Please select a face in Edit Mode.")
    return 

def Nurbs():
    
    return

def GenerateNurbsSolid():
    return

def ManualAdjustment():
    return

def GenerateClippedSurface():
    return

def GenerateNegative():
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

    return

def CutNurbs():
    return

def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO'):

    def draw(self, context):
        self.layout.label(text=message)


    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)


class SimplePropConfirmOperator(bpy.types.Operator):
    """Really?"""
    bl_idname = "test.custom_confirm_dialog"
    bl_label = "Do you really want to do that?"
    bl_options = {'REGISTER', 'INTERNAL'}

    prop1: bpy.props.BoolProperty()
    prop2: bpy.props.BoolProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        self.report({'INFO'}, "YES!")
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        row = self.layout
        row.prop(self, "prop1", text="Property A")
        row.prop(self, "prop2", text="Property B")

# class OBJECT_PT_CustomPanel(bpy.types.Panel):
#     bl_label = "My Panel"
#     bl_idname = "OBJECT_PT_custom_panel"
#     bl_space_type = "VIEW_3D"   
#     bl_region_type = "UI"
#     bl_category = "Tools"
#     bl_context = "objectmode"

#     def draw(self, context):
#         layout = self.layout
#         layout.operator(SimplePropConfirmOperator.bl_idname)

class Dialogue(bpy.types.Operator):
    bl_idname = "dialog.box"
    bl_label = "Dialog Box"
    
    text: bpy.props.StringProperty(name="Text:")

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

# Generates file browser pop-up window
class GenerateModels(Operator, ImportHelper):
    bl_idname = "test.open_filebrowser"
    bl_label = "Open the file browser (yay)"
    # user_input: bpy.props.StringProperty(name="User Input")

    filter_glob: StringProperty(
        default='*.glb',
        options={'HIDDEN'}
    )
    
    some_boolean: BoolProperty(
        name='Do a thing',
        description='Do a thing with the file you\'ve selected',
        default=True,
    )

                # Create and show the popup



    def execute(self, context):
        """Do something with the selected file(s)."""
        filename, extension = os.path.splitext(self.filepath)
        print('Selected file:', self.filepath)
        print('File name:', filename)
        print('File extension:', extension)
        print('Some Boolean:', self.some_boolean)
        
        # Import the selected file into Blender
        bpy.ops.import_scene.gltf(filepath=self.filepath)



        imported_object=SelectMesh() #integrated and working
        # def draw_func(self, context):
        #     self.layout.label(text="The object has been imported successfully.")
        #     self.layout.label(text="Click OK to continue.")

        # context.window_manager.invoke_props_dialog(self, draw_func)
        #Shows a message box with a specific message 
        bpy.ops.dialog.box('INVOKE_DEFAULT')
        ShowMessageBox("This is a message") 
        # bpy.ops.test.custom_confirm_dialog
        DrawRectangle(imported_object) #integrated and working
        GenerateBust(imported_object) #integrated and working
        AddThickness(imported_object) #integrated and working 
        SmoothSurface(imported_object) #integrated and working

        return {'FINISHED'}

def main():
    # Instantiate your file browser operation with arguments
    bpy.utils.register_class(GenerateModels)
    bpy.utils.register_class(Dialogue)
    # bpy.utils.register_class(OBJECT_PT_CustomPanel)
    # bpy.utils.register_class(SimplePropConfirmOperator)
    # bpy.ops.SimplePropConfirmOperator.bl_idname
    result = bpy.ops.test.open_filebrowser('INVOKE_DEFAULT')

if __name__ == "__main__":
    main()



# Run the code
file_path = "C:/Users/reece/Desktop/School or Extra/Coding Project/MK.glb"
clear_scene() #integrated and working
# import_glb() #not working: see note in code, this function seems to be run in parallel, so the code isn't waiting to return before continuing, so nothing below will work. 
# bpy.ops.import_scene.gltf(filepath=file_path)
# imported_object=SelectMesh() #integrated and working
# DrawRectangle(imported_object) #integrated and working
# GenerateBust(imported_object) #integrated and working
# AddThickness(imported_object) #integrated and working 
# SmoothSurface(imported_object) #integrated and working
# OrientFace() # Not Working
# Nurbs()
# ManualAdjustment()
# GenerateClippedSurface()
# GenerateNurbsSolid()
# SmoothSurface()
# GenerateNegative()
# CutNurbs()

