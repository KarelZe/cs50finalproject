import warnings

import quandl
from flask import render_template


def apology(top="", bottom=""):
    return render_template("apology.html", top=top, bottom=bottom)


def validate_form(form):
    # todo: error handling
    form['percentage'] = [float(i) for i in form['percentage']]

    # convert to int
    try:
        time = int(form['time'][0])
    except ValueError:
        time = -1

    if time not in range(1, 9999):
        form['time'] = -1
        warnings.warn("time out of boundary")
    else:
        form['time'] = time

    confidence = float(form['confidence'][0])
    if 0 >= confidence > 1:
        form['confidence'] = -1
        warnings.warn("confidence level out of boundary")
    else:
        form['confidence'] = confidence

    form = validate_symbol(form)
    form = validate_percentage(form)
    return form


def validate_percentage(form):
    len_percentage = len(form['percentage'])
    len_symbol = len(form['symbol'])

    # check if all given numbers are greater than 0
    valid_percentage = True
    for i in range(len_symbol):
        if form['percentage'][i] < 0:
            valid_percentage = False
            break

    # given input is incorrect, initialize list
    # with length of ticker list and weight equally
    if not (valid_percentage is True and
            sum(form['percentage']) == 1.0) and \
            len_symbol == len_percentage:
        form['percentage'] = [1] * len_symbol
        form['percentage'][:] = \
            [1.0 / len_symbol for _ in range(len_percentage)]
    return form


def validate_symbol(form):
    validated_symbol = []
    # loop through given symbols return validated list of symbols
    for i in range(len(form['symbol'])):
        try:
            data = quandl.get("WIKI/" + form['symbol'][i],
                              rows=1, column_index=0)
            if data is not None:
                validated_symbol.append("WIKI/" + form['symbol'][i])
        except:
            warnings.warn('error during validation')
        form['symbol'] = validated_symbol
        return form