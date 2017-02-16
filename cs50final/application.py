#!/usr/bin/env python3

import argparse
import json
from datetime import timedelta, date

import quandl

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
    # validate args
    helpers.print_args(args)
    # generate json
    var_to_json(100.0, 500.0, 20)


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

    data = [('year', 'future_value')]
    for i in range(time):
        portfolio_at_i = str(initial_value + (future_value - initial_value) / time * (i + 1))
        item = (str(date.today() + timedelta(days=i)), portfolio_at_i)
        data.append(item)
    var_json = json.JSONEncoder().encode(data)
    """
    target = open('var_to_json.json', 'w')
    target.write(var_json)
    target.close()
    """
    return var_json


if __name__ == "__main__":
    main()
