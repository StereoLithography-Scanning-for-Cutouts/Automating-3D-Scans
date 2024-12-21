import bpy

class MyClass(bpy.types.Operator):
    bl_idname = "dialog.box"
    bl_label = "Dialog Box"
    
    text: bpy.props.StringProperty(name="Text:")

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

# Register and call the operator
bpy.utils.register_class(MyClass)
bpy.ops.dialog.box('INVOKE_DEFAULT')