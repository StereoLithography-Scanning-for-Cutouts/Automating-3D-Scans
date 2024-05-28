##------------------------------------------
##Clearing the scene
##------------------------------------------

import bpy
import numpy as np
from mathutils import Vector

# Deselect all objects
bpy.ops.object.select_all(action='DESELECT')

# Select all objects in the scene
bpy.ops.object.select_all(action='SELECT')

# Delete selected objects
bpy.ops.object.delete()


# Import the file - currently doing manually 


#-----------------------------------------------
# This moves the selected face to the origin 
# and rotates it to be normal to the z-axis
#-----------------------------------------------

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

