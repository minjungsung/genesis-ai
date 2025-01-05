import threading
import time
import genesis as gs
import numpy as np
import argparse

gs.init(backend=gs.cpu)

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--vis", action="store_true", default=False)
args = parser.parse_args()

# Create a Scene with Viewer and Visualization Option
scene = gs.Scene(
    show_viewer=args.vis,
    viewer_options=gs.options.ViewerOptions(
        res=(1280, 960),
        camera_pos=(3.5, 0.0, 2.5),
        camera_lookat=(0.0, 0.0, 0.5),
        camera_fov=40,
        max_FPS=60,
    ),
    vis_options=gs.options.VisOptions(
        show_world_frame=True,
        world_frame_size=1.0,
        show_link_frame=False,
        show_cameras=False,
        plane_reflection=True,
        ambient_light=(0.1, 0.1, 0.1),
    ),
    renderer=gs.renderers.Rasterizer(),
)

# Add a Plane Entity to the Scene
plane = scene.add_entity(gs.morphs.Plane())

# Add a Franka Emika Panda Robot Entity from MJCF File
franka = scene.add_entity(gs.morphs.MJCF(file="xml/franka_emika_panda/panda.xml"))

# Add a Camera
cam = scene.add_camera(
    res=(640, 480),
    pos=(3.5, 0.0, 2.5),
    lookat=(0, 0, 0.5),
    fov=30,
    GUI=False,
)


# Define the run_simulation function before using it
def run_simulation(scene, cam, vis):
    cam.start_recording()
    for i in range(120):
        scene.step()
        cam.set_pose(
            pos=(3.0 * np.sin(i / 60), 3.0 * np.cos(i / 60), 2.5),
            lookat=(0, 0, 0.5),
        )
        cam.render()
        time.sleep(0.016)  # Sleep to simulate real-time (60 FPS)
    cam.stop_recording(save_to_filename="video.mp4", fps=60)
    if vis:
        scene.viewer.stop()


scene.build()

# Use threading to run the simulation in a separate thread
simulation_thread = threading.Thread(target=run_simulation, args=(scene, cam, args.vis))
simulation_thread.start()

# Start the viewer if visualization is enabled
if args.vis:
    scene.viewer.start()
