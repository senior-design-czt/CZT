from flask import Flask, request, jsonify, render_template, redirect, url_for, send_file
import os
from pathlib import Path
import matplotlib.pyplot as plt
import proto_ml_regression as ml
import numpy as np
import csv



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_DIR = os.path.join(Path.home(), 'czt')
app.config['TEMPLATES_AUTO_RELOAD'] = True

datafile = os.path.join(UPLOAD_DIR, 'data.csv')


@app.route('/home')
@app.route('/')
def home():
    """Serves the startup page for the website"""
    return render_template('home.html')


@app.route('/data')
def data():
    """Serves the data page for the website"""
    if os.path.isfile(datafile):
        with open(datafile, newline='') as f:
            csvfile = list(csv.reader(f))
            return render_template('data.html',
                                   render_table=True,
                                   header=csvfile[0],
                                   body=csvfile[1:])
    return render_template('data.html', render_table=False)


@app.route('/status')
def status():
    """Serves the status page for the website"""
    return render_template('status.html')


@app.route('/results')
def results():
    """Serves the results page for the website"""
    return render_template('results.html')


@app.route('/layout')
def layout():
    """Serves the layout page for the website"""
    return render_template('layout.html')


@app.route('/upload', methods=['POST'])
def upload():
    """
    This url is used to upload a new data file to the server.
    Requires a file input form named 'file' to read from.
    View https://www.tutorialspoint.com/flask/flask_file_uploading.htm for an example on how to use this.
    """
    if 'file' in request.files:
        f = request.files['file']
        f.save(datafile)
    return redirect(url_for('data'))


@app.route('/train')
def train():
    os.system('python3 proto_ml_regression.py impurities.csv output.txt 1.5')
    return redirect(url_for('results'))

@app.route('/results')
def compare():
    return render_template('compare.html')

@app.route('/results/graph')
def return_graph():
    # Grab results from regressor
    ml.RunRegressionAnalysis('impurities.csv', 'output.txt')
    impurities, coefficients = ml.GetImpurityCoefficientsForGraph()
    # Generate graph as png
    spacing = np.arange(len(coefficients[1:]))
    print(spacing, coefficients[1:])
    plt.bar(spacing, coefficients[1:], align='center', alpha=0.5)
    plt.xticks(spacing, impurities[1:])
    plt.xlabel('Impurity')
    plt.ylabel('Impact')
    plt.title('Effect of Impurities on Performance')
    filename = 'graph.png'
    plt.savefig(filename)
    # Send file to client
    try:
        return send_file(filename, attachment_filename='graph.png')
    except Exception as e:
        return str(e)

@app.route('/results/text')
def return_text():
    filename = 'output.txt'
    try:
        return send_file(filename, attachment_filename='output.txt')
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    if not os.path.isdir(UPLOAD_DIR):
        print('Doing directory setup for upload data')
        os.mkdir(UPLOAD_DIR)
    app.run(debug=True)
