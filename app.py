from flask import Flask, request
import os

app = Flask(__name__)


@app.route('/')
def index():
    """Serves the startup page for the website"""
    return app.send_static_file('index.html')


# info on uploading files: https://www.tutorialspoint.com/flask/flask_file_uploading.htm
@app.route('/upload', methods=['POST'])
def upload_data():
    f = request.files['file']


if __name__ == '__main__':
    app.run(debug=True)
