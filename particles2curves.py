# This script converts particle systems to individual curve objects. It was 
# based heavily on the particles to keyframes script by stackexchange user jasperge
# at http://blender.stackexchange.com/a/7142 , but this version gives you curve 
# objects instead. Like the original script, the animation start and stop times will
# set the range of points used for the curves. Select the object you wish to convert
# prior to running the script. 
#
# Got impatient wating for that new particle-node-editor feature that's been 
# rumored, this seemed like the simplest stop-gap approach. 

import bpy


def create_objects_for_particles(ps, totalFrames):
    # create a curve object for every particle
    obj_list = []
   
    for i, _ in enumerate(ps.particles):

        # create the Curve Datablock
        curveData = bpy.data.curves.new('myCurve', type='CURVE')
        curveData.dimensions = '3D'
        curveData.resolution_u = 2

        # map particle coords at each frame to spline
        polyline = curveData.splines.new('POLY')
        print(totalFrames)
        polyline.points.add(totalFrames-1) 
        #splines init with a point already


        #create the container object
        dupli = bpy.data.objects.new(
                    name="particle.{:03d}".format(i),
                    object_data=curveData)
       
        bpy.context.scene.objects.link(dupli)
        obj_list.append(dupli)
    return obj_list


def match_and_keyframe_objects(ps, obj_list, start_frame, end_frame):
    # Match and keyframe the objects to the particles for every frame in the
    # given range.
    for frame in range(start_frame, end_frame + 1):
        bpy.context.scene.frame_set(frame)
        for p, obj in zip(ps.particles, obj_list):
            #print obj.data.splines.points.length()
            obj.data.splines[0].points[frame].co = (p.location.x, p.location.y, p.location.z, 1)
   
   

def main():
    # The active object should be the one with the particle system.
    ps_obj = bpy.context.object
    #this line selects the replicated object. not using for now
    #obj = [obj for obj in bpy.context.selected_objects if obj != ps_obj][0]
    ps = ps_obj.particle_systems[0]  # Assume only 1 particle system is present.
    start_frame = bpy.context.scene.frame_start
    end_frame = bpy.context.scene.frame_end
    total_frames = end_frame-start_frame+1
    #frame inclusive 
    obj_list = create_objects_for_particles(ps, total_frames)
    
    match_and_keyframe_objects(ps, obj_list, start_frame, end_frame)

if __name__ == '__main__':
    main()
