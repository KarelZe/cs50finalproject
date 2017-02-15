#!/usr/bin/env python3

import argparse

import quandl
from flask import jsonify

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


def download_data(to_download):
    try:
        data = quandl.get(to_download.symbol)
        return data
    except:
        return None


def calculate_historical_var(stock_data, percentage, time):
    """ This is a very basic approach to calculate an "uncorrelated value at risk (time) expost" based on:
    "III. Ermittlung des Value at Risk mit Simulationsverfahren, Historische Simulation, VWA"
    This is for testing purpose only.
    :param stock_data: pandas.DataFrame for one or multiple stocks
    :param percentage: between 0 and 1.
    :param time: time in days
    :return: future_value
    """
    print(stock_data, percentage, time)
    return 0


def var_to_json(initial_value, future_value, time):
    """This function calculates a time series and writes it to a .json file. The file can then be used for
    google charts. The time series is calculated using linear interpolation.
    This is for testing purpose only.
    :param initial_value:
    :param future_value:
    :param time:
    :return:
    """
    print(initial_value, future_value, time)
    return jsonify("data")


if __name__ == "__main__":
    main()
