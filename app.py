from flask import Flask, request, jsonify
import os

app = Flask(__name__)

UPLOAD_DIR = os.getcwd() + '/data'
print (UPLOAD_DIR)

app.config['UPLOAD_FOLDER'] = UPLOAD_DIR


@app.route('/')
def index():
    """Serves the startup page for the website"""
    return app.send_static_file('index.html')


# info on uploading files: https://www.tutorialspoint.com/flask/flask_file_uploading.htm
@app.route('/upload', methods=['POST'])
def upload_data():
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
