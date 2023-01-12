import os
import sys
import cv2
import time
from multiprocessing import Pool
from itertools import repeat

# hacky way to import from parent directory
sys.path.insert(0, os.path.join("evd_3", "deep_learning"))
import augment_matrices
import image_augments
#
# Create a folder structure for YOLOv5 training
#

target_data_path = os.path.join(
    "evd_3", "deep_learning", "cnn_preperation", "data")
original_dataset_path = os.path.join("evd_3", "original_dataset")

generate_dataset = False

if not os.path.exists(target_data_path):
    for split in ['train', 'val', 'test']:
        for type in ['hangloose', 'paper', 'rock', 'scissors']:
            os.makedirs(os.path.join(target_data_path, split, type))
    generate_dataset = True

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
hangloose_images = get_filenames(
    os.path.join(original_dataset_path, 'hangloose'))
paper_images = get_filenames(os.path.join(original_dataset_path, 'paper'))
rock_images = get_filenames(os.path.join(original_dataset_path, 'rock'))
scissors_images = get_filenames(
    os.path.join(original_dataset_path, 'scissors'))


#
# Check for duplicates
#
duplicates = hangloose_images & paper_images & rock_images & scissors_images

print(duplicates)

# no duplicates found

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


types = {"hangloose": 0, "paper": 1, "rock": 2, "scissors": 3}


def generate_augmented(split, type, image_name):
    # Label filename
    label_name = image_name.replace('.jpg', '.txt')

    M = np.eye(3)
    M = np.matmul(M, augment_matrices.get_translate_matrix(0.5))
    M = np.matmul(M, augment_matrices.get_zoom_matrix())
    M = np.matmul(M, augment_matrices.get_stretch_matrix())
    M = np.matmul(M, augment_matrices.get_shear_matrix())
    M = np.matmul(M, augment_matrices.get_rotate_matrix(False))
    M = np.matmul(M, augment_matrices.get_flip_matrix())

    image = cv2.imread(os.path.join(original_dataset_path, type, image_name))
    height, width = image.shape[:2]

    imageMatrix = np.eye(3)

    imageMatrix = np.matmul(np.float32(
        [[1, 0, width / 2], [0, 1, height / 2], [0, 0, 1]]), M)  # type: ignore
    imageMatrix = np.matmul(imageMatrix, np.float32(
        [[1, 0, -width / 2], [0, 1, -height / 2], [0, 0, 1]]))  # type: ignore

    image = cv2.warpAffine(
        image, imageMatrix[:2], (width, height), borderMode=cv2.BORDER_REPLICATE)

    image = image_augments.rotate_hsv_random(image)
    image = image_augments.higher_contrast_random(image)
    image = image_augments.change_brightness_random(image)
    image = image_augments.add_noise_random(image)

    # Destination paths
    target_image_folder = os.path.join(
        target_data_path, split, type)

    # Copy image and overwrite or create label files
    # get timestamp in ms
    timestamp = time.time_ns()
    cv2.imwrite(os.path.join(target_image_folder,
                str(timestamp) + image_name), image)


def create_dataset(type, image_names, train_percentage, val_percentage, number_of_instances):
    number_of_instances_created = 0

    random_train_filenames = []
    random_val_filenames = []
    random_test_filenames = []

    while number_of_instances_created < number_of_instances:

        for i, image_name in enumerate(image_names):
            if '_ignore' in image_name:  # ignore images with _ignore in the name
                continue

            # Split into train, val, or test
            if number_of_instances_created < train_percentage * number_of_instances:
                random_train_filenames.append((i, image_name))
            elif number_of_instances_created < (train_percentage + val_percentage) * number_of_instances:
                random_val_filenames.append((i, image_name))
            else:
                random_test_filenames.append((i, image_name))

            number_of_instances_created += 1
            if (number_of_instances_created >= number_of_instances):
                break

    with Pool(20) as p:
        for split, filenames in zip(['train', 'val', 'test'], [random_train_filenames, random_val_filenames, random_test_filenames]):
            p.starmap(generate_augmented, zip(
                repeat(split), repeat(type), [x[1] for x in filenames]))


if generate_dataset:
    number_of_instances = 1000

    print("Creating hangloose dataset")
    startTime = time.time()
    create_dataset('hangloose', hangloose_images,
                   0.6, 0.2, number_of_instances)
    print("Creating hangloose dataset took: ", time.time() - startTime)

    print("Creating paper dataset")
    startTime = time.time()
    create_dataset('paper', paper_images, 0.6, 0.2, number_of_instances)
    print("Creating paper dataset took: ", time.time() - startTime)

    print("Creating rock dataset")
    startTime = time.time()
    create_dataset('rock', rock_images, 0.6, 0.2, number_of_instances)
    print("Creating rock dataset took: ", time.time() - startTime)

    print("Creating scissors dataset")
    startTime = time.time()
    create_dataset('scissors', scissors_images, 0.6, 0.2, number_of_instances)
    print("Creating scissors dataset took: ", time.time() - startTime)

else:
    print("dataset has already been created")
