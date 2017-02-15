#!/usr/bin/env python3

import argparse
import os
import warnings

from cs50final import helpers


def main():

    parser = argparse.ArgumentParser(
        description=(
            'Calculates a future value of a stock portfolio from given stock symbols'
        )
    )
    # symbol is positional, one or more symbols are saved to a list
    parser.add_argument('-s', '--symbol', nargs='*', type=str, default=[],
                        help="valid ticker symbol")
    # percentage of share in portfolio
    parser.add_argument('-p', '--percentage', nargs='*', type=float, default=[],
                        help="percentage level between 0.01 and 1")

    parser.add_argument('-c', '--confidence', nargs='?', type=helpers.check_confidence, default=0.5,
                        help="confidence level between 0.1 and 1")
    parser.add_argument('-t', '--time', nargs='?', type=helpers.check_time, default=250)
    parser.add_argument('-i', '--initial', nargs='?', type=float, default=100000.0)

    args = parser.parse_args()

    # validate arguments
    args = helpers.validate_args(args)

    # calculation
    # todo: implementation of download, montecarlo and jasonify
    # print input to screen
    helpers.print_args(args)


if __name__ == "__main__":
    main()
