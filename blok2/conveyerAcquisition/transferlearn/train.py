import os
# 
# Create a folder structure for YOLOv5 training
# 
if not os.path.exists('blok2/conveyerAcquisition/transferlearn/data'):
    for folder in ['images', 'labels']:
        for split in ['train', 'val', 'test']:
            os.makedirs(f'blok2/conveyerAcquisition/transferlearn/data/{folder}/{split}')

# 
# Check for duplicate images
# 
import glob

def get_filenames(folder):
    filenames = set()
    
    for path in glob.glob(os.path.join(folder, '*.png')):
        # Extract the filename
        filename = os.path.split(path)[-1]        
        filenames.add(filename)

    return filenames


# Dog and cat image filename sets
bag_images = get_filenames('blok2/conveyerAcquisition/datasets/bag')
bottle_images = get_filenames('blok2/conveyerAcquisition/datasets/bottle')
bottlecap_images = get_filenames('blok2/conveyerAcquisition/datasets/bottlecap')
fork_images = get_filenames('blok2/conveyerAcquisition/datasets/fork')
knife_images = get_filenames('blok2/conveyerAcquisition/datasets/knife')
pen_images = get_filenames('blok2/conveyerAcquisition/datasets/pen')
spoon_images = get_filenames('blok2/conveyerAcquisition/datasets/spoon')
styrofoam_images = get_filenames('blok2/conveyerAcquisition/datasets/styrofoam')


# 
# Check for duplicates
# 
duplicates = bag_images & bottle_images & bottlecap_images & fork_images & knife_images & pen_images & spoon_images & styrofoam_images

print(duplicates)

###  no duplicates found

# 
# Split Image and Label Files into Train, Val, and Test Sets
# 

import numpy as np

bag_images = np.array(list(bag_images))
bottle_images = np.array(list(bottle_images))
bottlecap_images = np.array(list(bottlecap_images))
fork_images = np.array(list(fork_images))
knife_images = np.array(list(knife_images))
pen_images = np.array(list(pen_images))
spoon_images = np.array(list(spoon_images))
styrofoam_images = np.array(list(styrofoam_images))


# Use the same random seed for reproducability
np.random.seed(42)
np.random.shuffle(bag_images)
np.random.shuffle(bottle_images)
np.random.shuffle(bottlecap_images)
np.random.shuffle(fork_images)
np.random.shuffle(knife_images)
np.random.shuffle(pen_images)
np.random.shuffle(spoon_images)
np.random.shuffle(styrofoam_images)


# 
# copy image and label files to the respective folders given train_size and val_size.
# 

import shutil

def split_dataset(type, image_names, train_size, val_size):
    for i, image_name in enumerate(image_names):

        if '_ignore' in image_name: # ignore images with _ignore in the name
            continue

        # Label filename
        label_name = image_name.replace('.png', '.txt')
        
        # Split into train, val, or test
        if i < train_size:
            split = 'train'
        elif i < train_size + val_size:
            split = 'val'
        else:
            split = 'test'
        
        # Source paths
        source_image_path = f'blok2/conveyerAcquisition/datasets/{type}/{image_name}'
        source_label_path = f'blok2/conveyerAcquisition/datasets/{type}/{label_name}'

        # Destination paths
        target_image_folder = f'blok2/conveyerAcquisition/transferlearn/data/images/{split}'
        target_label_folder = f'blok2/conveyerAcquisition/transferlearn/data/labels/{split}'

        # Copy files
        shutil.copy(source_image_path, target_image_folder)
        shutil.copy(source_label_path, target_label_folder)



# train_size is amount of images used for training
train_size = 1500 - 300 - 300 # 300(20%) for validation and 300(20%) for testing
val_size = 300


split_dataset('bag', bag_images, train_size=train_size, val_size=val_size)
split_dataset('bottle', bottle_images, train_size=train_size, val_size=val_size)
split_dataset('bottlecap', bottlecap_images, train_size=train_size, val_size=val_size)
split_dataset('fork', fork_images, train_size=train_size, val_size=val_size)
split_dataset('knife', knife_images, train_size=train_size, val_size=val_size)
split_dataset('pen', pen_images, train_size=train_size, val_size=val_size)
split_dataset('spoon', spoon_images, train_size=train_size, val_size=val_size)
split_dataset('styrofoam', styrofoam_images, train_size=train_size, val_size=val_size)
