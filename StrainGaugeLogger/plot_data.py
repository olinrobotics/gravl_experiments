#!/usr/bin/env python3

from numpy import genfromtxt
from argparse import ArgumentParser
import matplotlib.pyplot as plt
import csv


def generate_plot(t, N, title=''):
    """Create plot of Newtons over time."""
    plt.figure()
    plt.scatter(t, N)
    plt.title(title)
    plt.xlabel("Time (s)")
    plt.ylabel("Force (N)")
    plt.show()

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('data_file', type=str,
        help='filepath of csv data file')

    args = vars(parser.parse_args())
    data_file = args['data_file']
    data = genfromtxt(data_file, delimiter=',')
    t = data[:, 1]
    N = data[:, 0]
    p = generate_plot(t, N, title=data_file)
