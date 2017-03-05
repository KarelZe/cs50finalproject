#!/usr/bin/env python3

from datetime import timedelta, date

from flask import Flask, redirect, render_template, request, url_for, jsonify
from flask_jsglue import JSGlue

from cs50final import helpers

# configure application
app = Flask(__name__)
JSGlue(app)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response


def download_data(to_download):
    """try:
        data = quandl.get(to_download.symbol)
        return data
    except:
        return None"""
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
        helpers.validate_form(form)
        # run calculation 
        return var_to_json(100000, 150000, 5)
    else:
        return render_template('search.html')


if __name__ == "__main__":
    app.run(debug=True)
