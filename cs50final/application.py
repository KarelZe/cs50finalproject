#!/usr/bin/env python3

import os
from datetime import timedelta, date

import numpy as np
import pandas as pd
import quandl
from flask import Flask, redirect, render_template, request, url_for, jsonify
from flask_jsglue import JSGlue
from scipy.special import ndtri

from cs50final import helpers

# configure application
app = Flask(__name__)
JSGlue(app)

"""register for free on quandl.com to get an API_KEY. Set it as an environment variable"""
try:
    quandl.ApiConfig.api_key = os.environ.get("API_KEY")

except KeyError:
    raise RuntimeError("API_KEY not set")

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response


def calculate_historical_var(to_download):
    """ This is a very basic approach to calculate an "uncorrelated value at risk (time) expost" based on:
    "III. Ermittlung des Value at Risk mit Simulationsverfahren, Historische Simulation, VWA
    :param to_download: relevant calculation information including symbols, confidence, initial_capital etc.
    :return on success: to_download with calculated future value, otherwise NULL
    """
    try:
        df = quandl.get(to_download['symbol'], start_date="2013-12-25", end_date="2014-12-31", collapse="weekly",
                        transform="rdiff", returns="pandas")

        # slice data frame to relevant close quotes
        df_portfolio = df.ix[::, 10::12]

        # Transform percent matrix for multiplication
        df_multiplier = pd.DataFrame(to_download['percentage']).transpose()
        df_multiplier = df_multiplier * to_download['initial_capital']

        # multiply daily return in % with the total initial capital * percentage
        df_product = pd.DataFrame(df_multiplier.values * df_portfolio.values, columns=df_portfolio.columns,
                                  index=df_portfolio.index)

        # sum up daily return, calculate standard deviation
        df_product['sum_portfolio'] = df_product.sum(axis=1)
        std = df_product["sum_portfolio"].std()

        # value at risk scaled to horizon = value at risk * square root time
        value_at_risk = ndtri(1 - to_download['confidence']) * std * np.sqrt(to_download['time'])
        to_download['future_value'] = max(to_download['initial_capital'] + value_at_risk, 0)
        print(to_download['future_value'])
        return to_download
    except:
        return None


def var_to_json(initial_value, future_value, time):
    """This function calculates a time series and writes it to a .json file. The file can then be used for
    google charts. The time series is calculated using linear interpolation.
    This is for testing purpose only.
    :param initial_value:
    :param future_value:
    :param time:
    :return:
    """

    data = {'0_year': '0_future_value'}
    for i in range(time):
        value_at_i = str(initial_value + (future_value - initial_value) / time * (i + 1))
        key_at_i = str(date.today() + timedelta(days=i))
        data[key_at_i] = value_at_i
    return jsonify(data)


@app.route('/')
def index():
    # This function forwards to /search
    return redirect(url_for('search'))


@app.route('/search', methods=['GET', 'POST'])
def search():
    """This function function takes the input from the form, converts it to a dict and renders it as json"""
    if request.method == 'POST':
        """ convert from werkzeug multidict to dict nest everything in lists for easier parsing.
        Every element will be nested in a single list by default. """

        form = request.form.to_dict(flat=False)

        form['initial_capital'] = 100000

        helpers.validate_form(form)

        return jsonify(calculate_historical_var(form))
    else:
        return render_template('search.html')


if __name__ == "__main__":
    app.run(debug=True)
