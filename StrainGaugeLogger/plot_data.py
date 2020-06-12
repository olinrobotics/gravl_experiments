#!/usr/bin/env python3.6

from numpy import genfromtxt
from argparse import ArgumentParser
import matplotlib.pyplot as plt
import csv


def generate_plot(t, N, title='', xlabel='', ylabel=''):
    """Create plot of Newtons over time."""
    plt.figure()
    plt.scatter(t, N)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

if __name__ == "__main__":

    # Define and parse CLI
    parser = ArgumentParser()
    parser.add_argument('data_file', type=str,
        help='filepath of csv data file')
    args = vars(parser.parse_args())
    data_file = args['data_file']

    # Pull headers and data from CLI
    data = genfromtxt(data_file, delimiter=',')
    t = data[1:, 1]
    N = data[1:, 0]
    with open(data_file, 'r') as io_obj:
        reader = csv.reader(io_obj, delimiter=',')
        t_label, N_label = next(reader)

    p = generate_plot(t, N, xlabel=t_label, ylabel=N_label, title=data_file)
