from flask import Flask, request, jsonify, render_template
import os
from pathlib import Path


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
    if not 'file' in request.files:
        return jsonify(result="Fail", message="No form named 'file' to get file from")

    f = request.files['file']
    f.save(os.path.join(UPLOAD_DIR, f.filename))
    return jsonify(result="Success")


if __name__ == '__main__':
    if not os.path.isdir(UPLOAD_DIR):
        print('Doing directory setup for upload data')
        os.mkdir(UPLOAD_DIR)
    app.run(debug=True)
