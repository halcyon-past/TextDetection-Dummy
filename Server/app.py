from flask import Flask, request, send_file
from GPTmodel import initialize
from flask_cors import CORS
import openpyxl
import pandas as pd
import shutil
import os

app = Flask(__name__)
CORS(app, methods=['GET', 'POST'])
app.config['JSON_SORT_KEYS'] = False

path=['',]

@app.route("/", methods=['GET'])
def home():
    return "The Server is running on port 5000"

@app.route('/upload', methods=['POST'])
def upload_files():
    if request.method == 'POST':
        files = request.files.getlist('files')
        upload_folder = 'path'
        os.makedirs(upload_folder, exist_ok=True)
        initialize()
        for file in files:
            filename = file.filename
            file.save(os.path.join('path', filename))

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = 'Sheet1'
        wb.save('path\\result.xlsx')
            
        return 'Files uploaded successfully'
        
@app.route("/download/", methods=['GET'])
def download_file():
    if os.path.exists("path\\'result.xlsx'"):
        file_path = os.path.join('path', 'result.xlsx')
        return send_file(file_path, as_attachment=True)
    else:
        return 'No Such File Exists'

@app.route("/cleardata", methods=['GET'])
def clear_data():
    if os.path.exists('path'):
        shutil.rmtree('path')
        return "Data Cleared"
    else:
        return "No Data to Clear"

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0", port=5000)
