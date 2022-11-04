import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


def remove_out_liers(data):
    # get standard deviation of data
    std = data.std()
    mean = data.mean()
    # for every row in data
    for index, row in data.iteritems():
        # if the value is bigger or smaller than 3 std
        if row > (std * 3) + mean or row < (std * -3) + mean:
            # set row to none
            data[index] = None

    return data


if __name__ == '__main__':
    # get the data
    data = pd.read_csv(os.path.join('evd_3', 'pre_processing', 'data.csv'))

    # remove the first colom
    data = data.drop(data.columns[0], axis=1)

    # get the colom names
    colom_names = data.columns

    # remove the first row
    data = data.drop(data.index[0])

    total_datapoint_count = len(data)

    # split the data into different dataframes for each different gesture in the first colom (hangloose, ignore, paper, rock, scissors)
    hangloose = data[data['0'] == 'hangloose']
    ignore = data[data['0'] == 'ignore']
    paper = data[data['0'] == 'paper']
    rock = data[data['0'] == 'rock']
    scissors = data[data['0'] == 'scissors']

    # #  now remove outliers from the data wich ar bigger or smaller than 3 std
    for colom in colom_names:
        if colom == '0':
            continue
        hangloose[colom] = remove_out_liers(hangloose[colom])
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

    clean_datapoint_count = len(
        hangloose) + len(ignore) + len(paper) + len(rock) + len(scissors)
    print("outliers removed: {} out of {}".format(
        total_datapoint_count - clean_datapoint_count, total_datapoint_count))

    fig0, ax0 = plt.subplots(3, 2)

    # plot every colom into a histogram
    i = 0
    for colom in colom_names:
        if colom == '0':
            continue

        ax0[i // 2, i % 2].hist(hangloose[colom], bins=10,
                                alpha=0.5, label='hangloose')
        # plt.hist(ignore[colom], bins=10, alpha=0.5, label='ignore')
        ax0[i // 2, i % 2].hist(paper[colom], bins=10,
                                alpha=0.5, label='paper')
        ax0[i // 2, i % 2].hist(rock[colom], bins=10, alpha=0.5, label='rock')
        ax0[i // 2, i % 2].hist(scissors[colom], bins=10,
                                alpha=0.5, label='scissors')
        ax0[i // 2, i % 2].set_xlabel(colom)
        # ax0[0, 0].legend(loc='upper right')
        # ax0[0, 0].show()
        # ax0[0, 0].clf()
        i += 1

    fig0.show()

    plt.show()
