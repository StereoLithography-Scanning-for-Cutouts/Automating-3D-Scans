import bpy
from bpy.types import Operator
from bpy.props import StringProperty, BoolProperty
from bpy_extras.io_utils import ImportHelper
import os

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

def main():
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

if __name__ == "__main__":
    main()
