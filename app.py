from flask import Flask, render_template, request, send_file
import os
import easyocr
from IPython.display import Image

app = Flask(__name__)

@app.route("/")
def index():
    for filename in os.listdir('images/'):
        os.remove('images/' + filename)
    os.remove('output.txt')
    return render_template("upload.html")

@app.route("/upload", methods=["POST"])
def upload():
    target = 'images/'
    for file in request.files.getlist("file"):
        filename = file.filename
        dest = "/".join([target, filename])
        file.save(dest)
    return render_template("process.html")

@app.route("/process", methods=["GET"])
def process():
    l = ['hi','bn','te','ta','ar','mr']
    for i in l:
        reader = easyocr.Reader([i,'en'])
    # image file to be extracted
    file_name = "images/testmanu.jpg"
    Image(file_name)
    # extracted text
    ot = reader.readtext(file_name, detail=0)
    otext = ' '.join([str(elem) for elem in ot])
    encoded_unicode = otext.encode("utf8")
    a_file = open("output.txt", "wb")
    a_file.write(encoded_unicode)
    a_file = open("output.txt", "r")
    return render_template("download.html")

@app.route("/download", methods=["GET"])
def download():
    p = "output.txt"
    return send_file(p,as_attachment=True)

if __name__ == "__main__":
    app.run(debug=False)