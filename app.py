from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_DIR = '~/czt'


@app.route('/')
@app.route('/home')
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


# info on uploading files: https://www.tutorialspoint.com/flask/flask_file_uploading.htm
@app.route('/upload', methods=['POST'])
def upload():
    f = request.files['file']
    f.save(os.path.join(UPLOAD_DIR, f.filename))
    return 'saved'


@app.route('/data')
@app.route('/data/<filename>')
def get_file(filename=None):
    if filename is None:
        return jsonify(os.listdir(UPLOAD_DIR))
    else:
        filename = os.path.join(UPLOAD_DIR, filename)
        if not os.path.isfile(filename):
            return 'File does not exist'
        with open(filename, 'r') as f:
            return f.read()


if __name__ == '__main__':
    app.run(debug=True)
