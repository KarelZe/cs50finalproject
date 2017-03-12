import warnings

import quandl
from flask import render_template


def apology(top="", bottom=""):
    """ Function returns apology.html.
    :param top: UTF8-Smiley
    :param bottom: Explanation.
    :return: HTML-Template
    """
    return render_template("apology.html", top=top, bottom=bottom)


def validate_form(form):
    """ Function to check whether form input is valid.
    :param form:
    :return: form validated
    """
    # try conversion to float, otherwise apply equal distribution.
    try:
        form['percentage'] = [float(i) for i in form['percentage']]
    except ValueError:
        form['percentage'] = [1 for _ in form['percentage']]

    # convert to int, otherwise set to -1 one. Error page will be returned.
    try:
        time = int(form['time'][0])
    except ValueError:
        time = -1

    # If time out of bounds, error page will be returned.
    if time not in range(1, 9999):
        form['time'] = -1
        warnings.warn("time out of boundary")
    else:
        form['time'] = time

    # If confidence out of bounds, error page will be returned.
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
    """ Functions checks, whether percentage is valid.
     If not, portfolio gets equally weighted.
    :param form:
    :return: form validated
    """
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
    """ Query Quandl data base and fetch one column and one row.
    Write valid tickers to list. Valid list is returned.
    If list is empty an error page is returned.
    :param form:
    :return: form validated
    """
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