from glob import glob
import imageio
import os

def create_gif(image_list, gif_name):
    frames = []
    for image_name in image_list:
        frames.append(imageio.imread(image_name))
        # Save them as frames into a gif
    imageio.mimsave(gif_name, frames, 'GIF', fps = 120)

def list_images():
    files = []
    for file in glob('./*jpeg'):
        files.append(file)
    files.sort()
    return files

print('starting gif making')
images = list_images()
create_gif(images, 'test.gif')

print('starting deleting images')
for image in images:
    os.remove(image)