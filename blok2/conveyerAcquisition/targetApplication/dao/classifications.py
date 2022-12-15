# create a class for that stores or collects data from a file

# import the modules
import os
import sys
import time
import cv2
import json

# create class
class Classifications:
    def __init__(self):
        # get root path
        self.root_path = os.path.dirname(os.path.abspath(__file__))
        # check if the file exists
        if not os.path.isfile(self.root_path + '/classifications.json'):
            # create the file
            with open(self.root_path + '/classifications.json', 'w') as f:
                # write the json to the file
                json.dump([], f, indent=4)
                


    # method that gets all the classifications
    def get_all(self):
        '''	
          Method that gets all the classifications
          :return: all the classifications
        '''
        # open the file
        with open(self.root_path + '/classifications.json') as f:
            # load the json
            data = json.load(f)
            # return the data
            return data
        
    # method that gets the last classification
    def get_last(self):
        '''
          Method that gets the last classification
          :return: the last classification
        '''
        # open the file
        with open(self.root_path + '/classifications.json') as f:
            # load the json
            data = json.load(f)
            # check if there are classifications
            if len(data) > 0:
                # return the last classification
                return data[-1]
            # return false if not found
            return False

    # method that adds a classification
    def insert(self, classificationArray):
        '''
          Method that adds a classification
          :param classificationArray array with an object with label and percentage
          :return: the new classification
        '''
        # open the file
        with open(self.root_path + '/classifications.json') as f:
            # load the json
            data = json.load(f)
            # create the new classification

            current_timestamp = time.time()*1000
            # converted to int
            current_timestamp = int(current_timestamp)

            newClassification = {
                'id': len(data) + 1,
                'classification': classificationArray,
                'timestamp': current_timestamp
            }
            # append the new classification to the data
            data.append(newClassification)
        # open the file
        with open(self.root_path + '/classifications.json', 'w') as f:
            # dump the data to the file
            json.dump(data, f, indent=4)
            # return the new classification
            return newClassification



    # method that saves a classification image
    def save_image(self, image):
        '''
          Method that saves a classification image
          :param image: the open cv image
          :return: the path of the image
        '''
        # get the current epoch time
        current_timestamp = time.time()*1000
        # converted to int
        current_timestamp = int(current_timestamp)
        # create the path
        path = self.root_path + '/images/' + str(current_timestamp) + '.jpg'
        # save the image
        cv2.imwrite(path, image)
        # return the path
        return path

    # method that gets the last classification image
    def get_last_image(self):
        '''
          Method that gets the last classification image
          :return: the path of the image
        '''
        # get all the images
        images = os.listdir(self.root_path + '/images')
        # check if there are images
        if len(images) > 0:
            # remove the .jpg from the images
            images = [image.replace('.jpg', '') for image in images]
            # get the last made image or the image with the highest timestamp
            last_image = max(images)
            # add the .jpg to the image
            last_image = last_image + '.jpg'
            # retun the image path
            path = self.root_path + '/images/' + last_image
            return path

        # return false if there are no images
        return False