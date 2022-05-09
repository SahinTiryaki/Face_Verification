from flask import Flask, jsonify, render_template, request, flash
import os
from face import predict
app = Flask(__name__)

UPLOAD_FOLDER = 'C:/Users/sahin/Desktop/face-verification-github/static/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route("/", methods = ["GET","POST"])
def homepage():
    return render_template("index.html")


@app.route("/predict", methods = ["POST","GET"])
def uploadPredict():
    if request.method == 'POST':
        print(request.files)
        if 'file1' not in request.files or 'file2' not in request.files:
            return render_template("predict.html", msg = "Bad")
        
       
        # file1
        file1 = request.files['file1']
        if file1.filename == '':
            return render_template("predict.html",msg = 'File 1 No selected file')
        if  file1.filename.split(".")[-1] not in  ALLOWED_EXTENSIONS:
            return render_template("predict.html",msg = 'File 1 extensions is not allowed, please upload png, jpeg pr jpg')
        file1.filename = "known_img.png"

        path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        file1.save(path)

        # file2
        file2 = request.files['file2']
        if file2.filename == '':
            return render_template("predict.html",msg = 'File 2 No selected file')
        if  file2.filename.split(".")[-1] not in  ALLOWED_EXTENSIONS:
            return render_template("predict.html",msg = 'File 2 extensions is not allowed, please upload png, jpeg pr jpg')
        file2.filename = "candicate_img.png"

        path = os.path.join(app.config['UPLOAD_FOLDER'], file2.filename)
        file2.save(path)
        
        result = predict(file1.filename, file2.filename)
        
        return render_template("predict.html", msg = result, img1 = f"{file1.filename}", img2 = f"{UPLOAD_FOLDER}{file2.filename}")
    
    return '''
    <h1> You can  use   only post</h1>

    '''

if __name__ == "__main__":
    app.secret_key = 'super secret key'

    app.run(debug=True, threaded=True, port = "8080", host="0.0.0.0")