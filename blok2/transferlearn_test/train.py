import os
# 
# Create a folder structure for YOLOv5 training
# 
if not os.path.exists('data'):
    for folder in ['images', 'labels']:
        for split in ['train', 'val', 'test']:
            os.makedirs(f'data/{folder}/{split}')

# 
# Check for duplicate images
# 
import glob

def get_filenames(folder):
    filenames = set()
    
    for path in glob.glob(os.path.join(folder, '*.jpg')):
        # Extract the filename
        filename = os.path.split(path)[-1]        
        filenames.add(filename)

    return filenames


# Dog and cat image filename sets
hangloose_images = get_filenames('original_dataset/hangloose')
paper_images = get_filenames('original_dataset/paper')
rock_images = get_filenames('original_dataset/rock')
scissors_images = get_filenames('original_dataset/scissors')


# 
# Check for duplicates
# 
duplicates = hangloose_images & paper_images & rock_images & scissors_images

print(duplicates)

###  no duplicates found

# 
# Split Image and Label Files into Train, Val, and Test Sets
# 

import numpy as np

hangloose_images = np.array(list(hangloose_images))
paper_images = np.array(list(paper_images))
rock_images = np.array(list(rock_images))
scissors_images = np.array(list(scissors_images))

# Use the same random seed for reproducability
np.random.seed(42)
np.random.shuffle(hangloose_images)
np.random.shuffle(paper_images)
np.random.shuffle(rock_images)
np.random.shuffle(scissors_images)


# 
# copy image and label files to the respective folders given train_size and val_size.
# 

import shutil

def split_dataset(type, image_names, train_size, val_size):
    for i, image_name in enumerate(image_names):
        # Label filename
        label_name = image_name.replace('.jpg', '.txt')
        
        # Split into train, val, or test
        if i < train_size:
            split = 'train'
        elif i < train_size + val_size:
            split = 'val'
        else:
            split = 'test'
        
        # Source paths
        source_image_path = f'original_dataset/{type}/{image_name}'
        source_label_path = f'original_dataset/{type}/{label_name}'

        # Destination paths
        target_image_folder = f'data/images/{split}'
        target_label_folder = f'data/labels/{split}'

        # Copy files
        shutil.copy(source_image_path, target_image_folder)
        shutil.copy(source_label_path, target_label_folder)



# train_size is amount of images - 50 for each class with 25% for validation and 25% for testing
split_dataset('hangloose', hangloose_images, train_size=(168-50), val_size=25)
split_dataset('paper', paper_images, train_size=(163-50), val_size=25)
split_dataset('rock', rock_images, train_size=(151-50), val_size=25)
split_dataset('scissors', scissors_images, train_size=(152-50), val_size=25)

