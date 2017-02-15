import os
import warnings
import quandl
import argparse


def validate_args(args):
    args = validate_percentage(args)
    args = validate_symbol(args)
    return args


def validate_percentage(args):
    # todo: rewrite code flat is better than nested

    len_percentage = len(args.percentage)
    len_symbol = len(args.symbol)

    if len(args.symbol) != 0 and len_symbol == len_percentage:

        # check if all given numbers are greater than 0
        valid_percentage = True
        for i in range(len_symbol):
            if args.percentage[i] < 0:
                valid_percentage = False
                break

        # check if total sum is equal to 1, if not weight portfolio equally
        if not (valid_percentage is True and sum(args.percentage) == 1.0):
            # warnings.warn('portfolio weighted equally due to invalid or missing options (-p)')
            args.percentage = [1] * len_symbol
            args.percentage[:] = [x / len_symbol for x in args.percentage]
    else:
        # given input is incorrect, initialize list with length of ticker list and weight equally
        # warnings.warn('portfolio weighted equally due to invalid or missing options (-p)')
        args.percentage = [1] * len_symbol
        args.percentage[:] = [x / len_symbol for x in args.percentage]
    return args


def validate_symbol(args):
    # todo try alternative approach https://github.com/quandl/quandl-python/blob/master/FOR_DEVELOPERS.md
    try:
        quandl.ApiConfig.api_key = os.environ.get("API_KEY")
    except KeyError:
        raise RuntimeError("API_KEY not set")

    validated_symbol = []
    # loop through given symbols return validated list of symbols
    # todo improve performance of query
    for i in range(len(args.symbol)):
        try:
            data = quandl.get("WIKI/" + args.symbol[i], rows=1)
            if data is not None:
                validated_symbol.append(args.symbol[i])
        except:
            warnings.warn('error during validation')
    args.symbol = validated_symbol
    return args


def check_confidence(value):
    fvalue = float(value)
    if fvalue <= 0.001 or fvalue > 1:
        raise argparse.ArgumentTypeError("%s confidence level out of boundary" % value)
    return fvalue


def check_time(value):
    ivalue = int(value)
    if ivalue <= 1 or ivalue > 99999:
        raise argparse.ArgumentTypeError("%s time out of boundary" % value)
    return ivalue

# print args to screen
def print_args(args):
    print(args)
    return None
