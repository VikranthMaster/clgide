from flask import Flask, render_template, request, Response, send_from_directory
import pandas as pd
import os
import uuid

app = Flask(__name__, template_folder="templates")

@app.route("/", methods = ["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("index.html", name = "Vikrath", age = 18)
    elif request.method == "POST":
        # username = request.form.get('username') #both are correct
        username = request.form['username']
        password = request.form.get('password')
        if username == "something" and password == "something":
            return "Success"
        else:
            return "Fail"
        
@app.route("/file", methods = ['GET', 'POST'])
def file():
    files = request.files['file']
    if files.content_type == "text/plain":
        return files.read().decode()

@app.route("/convert", methods = ['POST'])
def convert():
    file = request.files['file']
    df = pd.read_csv(file)
    
    response = Response(
        df.to_csv(),
        mimetype='text/csv',
        headers={
            'Content-Disposition':"attachment; filename=result.csv"
        }
    )
    
    return response

@app.route("/download", methods = ['POST'])
def download():
    file = request.files['file']
    df = pd.read_csv(file)
    
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    
    filename = f'{uuid.uuid4()}.csv'
    df.to_csv(os.path.join('downloads',filename))
    
    return render_template('download.html', filename=filename)

@app.route("/download1/<filename>")
def download1(filename):
    return send_from_directory('downloads', filename, download_name='result.csv')

if __name__ == "__main__":
    app.run(debug=True)