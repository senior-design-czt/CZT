from flask import Flask, request, jsonify, render_template
import os
from pathlib import Path
import matplotlib.pyplot as plt
import proto_ml_regression as ml
import numpy as np


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_DIR = os.path.join(Path.home(), 'czt')
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/home')
@app.route('/')
def home():
    """Serves the startup page for the website"""
    return render_template('home.html')


@app.route('/data')
def data():
    """Serves the data page for the website"""
    return render_template('data.html')


@app.route('/status')
def status():
    """Serves the status page for the website"""
    return render_template('status.html')


@app.route('/compare')
def compare():
    """Serves the compare page for the website"""
    return render_template('compare.html')


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
    if 'file' not in request.files:
        return jsonify(result="Fail", message="No form named 'file' to get file from")

    f = request.files['file']
    f.save(os.path.join(UPLOAD_DIR, f.filename))
    return jsonify(result="Success")


@app.route('/train')
def train():
    pass

@app.route('/compare')
def compare():
    return render_template('compare.html')

@app.route('/compare/graph')
def return_graph():
    # Grab results from regressor
    impurities, coefficients = ml.GetImpurityCoefficientsForGraph()
    # Generate graph as png
    spacing = range(len(impurities))
    plt.bar(spacing, coefficients, align='center', alpha=0.5)
    plt.xticks(spacing, impurities)
    plt.xlabel('Impurity')
    plt.ylabel('Impact')
    plt.title('Effect of Impurities on Performance')
    filename = os.path.join(UPLOAD_DIR, 'graph.png')
    plt.savefig(filename)
    # Send file to client
	try:
		return send_file(filename, attachment_filename='graph.png')
	except Exception as e:
		return str(e)

@app.route('/compare/text')
def return_text():
    filename = os.path.join(UPLOAD_DIR, 'output.txt')
	try:
		return send_file(filename, attachment_filename='output.txt')
	except Exception as e:
		return str(e)


if __name__ == '__main__':
    if not os.path.isdir(UPLOAD_DIR):
        print('Doing directory setup for upload data')
        os.mkdir(UPLOAD_DIR)
    app.run(debug=True)
