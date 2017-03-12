#!/usr/bin/env python3
import json
import os
from datetime import timedelta, date

import numpy as np
import pandas as pd
import quandl
from flask import Flask, redirect, render_template, request, url_for
from flask_jsglue import JSGlue
from scipy.special import ndtri

from cs50final import helpers

# configure application
app = Flask(__name__)
JSGlue(app)

# TODO: handle errors like: helpers.apology("(≥o≤)", "done.")

"""register for free on quandl.com to get an API_KEY.
 Set it as an environment variable"""
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


def calculate_historical_var(form):
    """ This is a very basic approach to calculate an "uncorrelated value
     at risk (time) expost" based on: "III. Ermittlung des Value at Risk
      mit Simulationsverfahren, Historische Simulation, VWA
    :param form: relevant calculation information including symbols,
     confidence, initial_capital etc.
    :return on success: to_download with calculated future value,
     otherwise NULL"""
    form['initial_capital'] = 100000
    try:
        df = quandl.get(form['symbol'], start_date="2013-12-25",
                        end_date="2014-12-31", collapse="weekly",
                        transform="rdiff", returns="pandas")

        # slice data frame to relevant close quotes
        df_portfolio = df.ix[::, 10::12]

        # Transform percent matrix for multiplication
        df_multiplier = pd.DataFrame(form['percentage']).transpose()
        df_multiplier = df_multiplier * form['initial_capital']

        # multiply daily return in % with the total initial capital * percentage
        df_product = pd.DataFrame(df_multiplier.values * df_portfolio.values,
                                  columns=df_portfolio.columns,
                                  index=df_portfolio.index)

        # sum up daily return, calculate standard deviation
        df_product['sum_portfolio'] = df_product.sum(axis=1)
        std = df_product["sum_portfolio"].std()

        # value at risk scaled to horizon = value at risk * square root time
        value_at_risk = ndtri(1 - form['confidence']) * std * np.sqrt(form['time'])
        form['future_value'] = max(form['initial_capital'] + value_at_risk, 0)
        return form
    except ValueError:
        return None


def var_to_json(initial_value, future_value, time):
    """This function calculates a time series and returns a json string.
    The json can be used for google charts. The time series is calculated
    using interpolation with square root.
    :param initial_value:
    :param future_value:
    :param time:
    :return:
    """

    factor = (future_value - initial_value) / np.sqrt(time)
    data = [[str(date.today() + timedelta(days=i)),
             initial_value + factor * np.sqrt(i)]
            for i in range(0, int(time))]
    return json.dumps(data)


@app.route('/')
def index():
    """This function forwards to /search"""
    return redirect(url_for('search'))


@app.route('/search', methods=['GET', 'POST'])
def search():
    """This function function takes the input from the form,
     converts it to a dict and renders it as json"""
    if request.method == 'POST':
        """convert from werkzeug multidict to dict
        nest everything in lists for easier parsing.
        Every element will be nested in a single list by default."""

        form = request.form.to_dict(flat=False)
        form = helpers.validate_form(form)
        form = calculate_historical_var(form)
        json_data = var_to_json(form['initial_capital'],
                                form['future_value'],
                                form['time'])
        # Todo: send calculation data to html
        return render_template('result.html', json_data=json_data)
    else:
        return render_template('search.html')


if __name__ == "__main__":
    # TODO: Disable for production use.
    app.run(debug=True)
