import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def remove_out_liers(data):
    # get standard deviation of data 
    std = data.std()
    # for every row in data
    for index, row in data.iteritems():
        # if the value is bigger or smaller than 3 std
        if row > (std * 3) or row < (std * -3):
            # set row to none 
            data[index] = None

    data
    return data

if __name__ == '__main__':
    # get the data
    data = pd.read_csv('evd_3\pre_processing\data.csv')

    # remove the first colom
    data = data.drop(data.columns[0], axis=1)

    # get the colom names
    colom_names = data.columns

    # remove the first row 
    data = data.drop(data.index[0])

    # split the data into different dataframes for each different gesture in the first colom (hangloose, ignore, paper, rock, scissors)
    hangloose = data[data['0'] == 'hangloose']
    ignore = data[data['0'] == 'ignore']
    paper = data[data['0'] == 'paper']
    rock = data[data['0'] == 'rock']
    scissors = data[data['0'] == 'scissors']


    # # plot every colom into a histogram
    # for colom in colom_names:
    #     if colom == '0':
    #         continue
    #     plt.hist(hangloose[colom], bins=10, alpha=0.5, label='hangloose')
    #     # plt.hist(ignore[colom], bins=10, alpha=0.5, label='ignore')
    #     plt.hist(paper[colom], bins=10, alpha=0.5, label='paper')
    #     plt.hist(rock[colom], bins=10, alpha=0.5, label='rock')
    #     plt.hist(scissors[colom], bins=10, alpha=0.5, label='scissors')
    #     plt.title(colom)
    #     plt.legend(loc='upper right')
    #     plt.show()
    #     plt.clf()


    #  now remove outliers from the data wich ar bigger or smaller than 3 std
    for colom in colom_names:
        if colom == '0':
            continue        
        ignore[colom] = remove_out_liers(ignore[colom])
        paper[colom] = remove_out_liers(paper[colom])
        rock[colom] = remove_out_liers(rock[colom])
        scissors[colom] = remove_out_liers(scissors[colom])

    # Remove every row with a none value because it is under standard deviation
    hangloose = hangloose.dropna()
    ignore = ignore.dropna()
    paper = paper.dropna()
    rock = rock.dropna()
    scissors = scissors.dropna()


    # plot every colom into a histogram
    for colom in colom_names:
        if colom == '0':
            continue
        plt.hist(hangloose[colom], bins=10, alpha=0.5, label='hangloose')
        # plt.hist(ignore[colom], bins=10, alpha=0.5, label='ignore')
        plt.hist(paper[colom], bins=10, alpha=0.5, label='paper')
        plt.hist(rock[colom], bins=10, alpha=0.5, label='rock')
        plt.hist(scissors[colom], bins=10, alpha=0.5, label='scissors')
        plt.title(colom)
        plt.legend(loc='upper right')
        plt.show()
        plt.clf()





# ''' 
#     Remove outliers from the data set.
#     The outliers are defined as the data points that are more than 3 standard deviations away from the mean.
#     The outliers are removed from the data set.
# '''
# from pstats import Stats
# from matplotlib import pyplot as plt
# import numpy as np
# import pandas as pd
# import cv2


# def remove_outliers():
#     # import the data
#     df = pd.read_csv('evd_3\pre_processing\data.csv')
#     # remove the first column (id)
#     df = df.drop(df.columns[0], axis=1)
#     # remove the first row (identifier)
#     df = df.drop(df.index[0])
#     # convert to numpy array
#     data = df.to_numpy()
#     # remove outliers per type (hangloose, ignore, paper, rock, scissors) (first column)
#     types = ['hangloose', 'ignore', 'paper', 'rock', 'scissors']
#     for i in range(1, 6):
#         # skip ignore 
#         if i == 2:
#             continue
#         # get the data for the current type
#         data_type = data[data[:, 0] == types[i-1]]
#         # remove the first column (type)
#         data_type = data_type[:, 1:]

#         # turn all values to float due to np.std needs float
#         data_type = data_type.astype(np.float)


#         # get the mean and standard deviation
#         mean = np.mean(data_type, axis=0)
#         std = np.std(data_type, axis=0)

#         # show standard deviation garph before removing outliers
#         a = std[0]
#         plt.plot(std[0], mean[0])
#         plt.title('0 before')
#         plt.show()
#         plt.clf()

#         plt.plot(std[1])
#         plt.title('1 before')
#         plt.show()
#         plt.clf()

#         plt.plot(std[2])
#         plt.title('2 before')
#         plt.show()
#         plt.clf()

#         plt.plot(std[3])
#         plt.title('3 before')
#         plt.show()
#         plt.clf()

#         plt.plot(std[4])
#         plt.title('4 before')
#         plt.show()
#         plt.clf()

#         # plt.plot(std[5])
#         # plt.title('5 before')
#         # plt.show()

#         # remove outliers
#         data_type = data_type[abs(data_type - mean) < 3 * std]
#         # remove nan values
#         data_type = data_type[~np.isnan(data_type).any(axis=1)]
#         # remove the outliers from the original data
#         data = np.delete(data, np.where(data[:, 0] == types[i-1]), axis=0)
#         data = np.concatenate((data, data_type), axis=0)
#         plt.show()

#         # remove outliers
#         data_type = data_type[~((data_type - mean) > 3 * std).any(axis=1)]
#         # get the mean and standard deviation
#         mean = np.mean(data_type, axis=0)
#         std = np.std(data_type, axis=0)

#         # show standard deviation garph after removing outliers
#         plt.plot(std)
#         plt.title('Standard deviation after removing outliers')
#         plt.show()

#         # cv wait key to show the plots
#         key = cv2.waitKey(0)
#         if key == ord('q'):
#             continue

#         # replace the data for the current type
#         data[data[:, 0] == str(i)] = data_type

#     # remove the rows with all zeros
#     data = data[~np.all(data == 0, axis=1)]
#     # convert to dataframe
#     df = pd.DataFrame(data)
#     # add the identifier
#     df = pd.concat([pd.DataFrame(['', '1', '2', '3', '4', '5', '6']), df])
#     # add the column names
#     df.columns = ['type', 'mean', 'std', 'skew', 'kurtosis', 'entropy', 'energy', 'contrast', 'homogeneity', 'correlation']
#     # save the data
#     df.to_csv('evd_3\pre_processing\data2.csv', index=False)




# if __name__ == '__main__':
#     remove_outliers()
