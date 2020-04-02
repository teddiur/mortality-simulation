from glob import glob
import imageio

def create_gif(image_list, gif_name):
    frames = []
    for image_name in image_list:
        frames.append(imageio.imread(image_name))
        # Save them as frames into a gif
    imageio.mimsave(gif_name, frames, 'GIF', fps = 60)

def list_images():
    files = []
    for file in glob('./*jpeg'):
        files.append(file)
    files.sort()
    return files

create_gif(list_images(), 'test.gif')
