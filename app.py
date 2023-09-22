from flask import Flask, render_template, request, send_from_directory
import pandas as pd
import os
import re

app = Flask(__name__)
UPLOAD_FOLDER = '.'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        excel_file = request.files['file']
        regex_pattern = request.form['regex']
        regex_pattern = re.compile(regex_pattern)
        if excel_file:
            filepath = os.path.join(UPLOAD_FOLDER, excel_file.filename)
            excel_file.save(filepath)
            df = pd.read_excel(filepath, engine='openpyxl')
            df = df.iloc[:, 0:5]
            df.columns = [x.replace("&", "").replace("\n", "") for x in df.columns]
            column = request.form['column']
            df['company'] = df[column].apply(
                lambda x: regex_pattern.search(str(x)).group(1) if regex_pattern.search(str(x)) else "")
            df['location'] = df[column].apply(
                lambda x: regex_pattern.search(str(x)).group(2) if regex_pattern.search(str(x)) else "")
            output_filepath = os.path.join(UPLOAD_FOLDER, "output_" + excel_file.filename)
            df.to_excel(output_filepath, index=False, engine='openpyxl')
            uploads = os.path.join(app.root_path, UPLOAD_FOLDER)
            return send_from_directory(directory=uploads, path="output_" + excel_file.filename)
            # return send_from_directory(output_filepath, as_attachment=True)
    return '<!DOCTYPE html><html><head><title>Regex Extractor for Excel</title></head><body><h2>Upload Excel File</h2><form action="/" method="post" enctype="multipart/form-data"><input type="file" name="file" required><br><br><label for="column">Select Column:</label><input type="text" name="column" value="Company  Location" required><br><br><label for="regex">Enter Regex Pattern:</label><input type="text" name="regex" value="(^.*[a-z\d]{1})([A-Z]{1}.*)" required><br><br><input type="submit" value="Extract"></form></body></html>'

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
