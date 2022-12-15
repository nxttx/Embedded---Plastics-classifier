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

    # method that gets a classification by id
    def get_by_id(self, id):
        '''
          Method that gets a classification by id
          :param id: the id of the classification
          :return: the classification
        '''
        # open the file
        with open(self.root_path + '/classifications.json') as f:
            # load the json
            data = json.load(f)
            # loop through the data
            for classification in data:
                # check if the id is the same
                if classification['id'] == id:
                    # return the data
                    return classification
            # return false if not found
            return False

    # method that adds a classification
    def insert(self, label, xc, yc, w, h, percentage):
        '''
          Method that adds a classification
          :param label the type of the classification
          :param xc: the centerd x coordinate of the classification (normalized)
          :param yc: the centerd y coordinate of the classification (normalized)
          :param w: the width of the classification (normalized)
          :param h: the height of the classification (normalized)
          :param percentage: the percentage of the certenty classification
          :return: the new classification
        '''
        # open the file
        with open(self.root_path + '/classifications.json') as f:
            # load the json
            data = json.load(f)
            # create the new classification
            newClassification = {
                'id': len(data) + 1,
                'label': label,
                'xc': xc,
                'yc': yc,
                'w': w,
                'h': h,
                'percentage': percentage,
                'current_timestamp': time.time()
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
        # get the current timestamp
        current_timestamp = time.time()
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
            # get the last image
            last_image = images[-1]
            # return the path
            return self.root_path + '/images/' + last_image
        # return false if there are no images
        return False
