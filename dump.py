bl_info = {
    "name": "Dump Edges Anim",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy
import bmesh
from bpy_extras.object_utils import world_to_camera_view


class ObjectDumpEdges(bpy.types.Operator):
    """Dump Edges Animation Script"""
    bl_idname = "object.dump_edges"
    bl_label = "Dump Edges in Animation"
    bl_options = {'REGISTER'}

    def execute(self, context):

        f = open("C:\\Users\\Kevin\\Documents\\osciMusic\\points.txt", "w+")

        scene = context.scene
        render = scene.render
        res_x = render.resolution_x
        res_y = render.resolution_y

        camera = bpy.data.objects['Camera']
        obj = bpy.data.objects['Cube']

        for edge in obj.data.edges:
            v1id = edge.vertices[0]
            v2id = edge.vertices[1]
            f.write("{},{}\n".format(v1id, v2id))
            
        f.write("\n")

        verts = (vert.co for vert in obj.data.vertices)
        coords_2d = [world_to_camera_view(scene, camera, coord) for coord in verts]

        for x, y, z in coords_2d:
            f.write("{},{}\n".format(x, y))

        f.close()

        return {'FINISHED'}

def register():
    bpy.utils.register_class(ObjectDumpEdges)

def unregister():
    bpy.utils.unregister_class(ObjectDumpEdges)

if __name__ == "__main__":
    register()