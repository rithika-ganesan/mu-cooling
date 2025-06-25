#############################################
#                                           #
#              Make animations              #
#                                           #
#############################################

from PIL import Image
import glob
import re
import os

directory_path='../plots/f3/*'
image_paths = sorted(glob.glob(directory_path))

sorted_files = sorted(
    image_paths,
    key=lambda x: int(re.search(r'\d+', os.path.basename(x)).group())
)

#image_paths_0 = sorted_files[0:200]
#image_paths_1 = sorted_files[200:]

images = [Image.open(p) for p in sorted_files]
#images_ = [Image.open(p) for p in image_paths_1]

#images.append(images_)

# Step 3: Save as GIF
# Use images[0] as the base, and append the rest
images[0].save(
    '../plots/btnorm-reg.gif',
    save_all=True,
    append_images=images[1:], 
    duration=100,   # Duration per frame in milliseconds
    loop=0          # Loop forever (use 1 to loop once)
)

