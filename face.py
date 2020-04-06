import os
from flask import Flask, flash, redirect, url_for, request, render_template
import sqlite3 as sql
import urllib
import json
import cv2
app = Flask(__name__)

app.secret_key = 'random string'
app.config["UPLOAD_FOLDER"]= 'store'
app.config["TEST_FOLDER"] = 'test'
tests_dir = 'C:/face_recog/test'
uploads_dir = 'C:/face_recog/store'
UPLOADED_FILES_DEST=uploads_dir
haar_cascade_face = cv2.CascadeClassifier('C:/face_recog/Face-Detection-in-Python-using-OpenCV-master/data/haarcascades/haarcascade_frontalface_default.xml')

@app.route('/process')  
def process():
    print('HELLO')
    return render_template('testupload.html') 

@app.route('/detect', methods = ['POST','GET'])
def detect():
    if request.method == 'POST':
        
        fi = request.files['img1']
        url = os.path.join(app.config['TEST_FOLDER'],fi.filename)
        fi.save(url)
        test_img = cv2.imread(url)
        test_img_gray = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
        rects = haar_cascade_face.detectMultiScale(test_img_gray, scaleFactor=1.1, minNeighbors=5,minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
        test_img = cv2.cvtColor(test_img, cv2.COLOR_BGR2RGB)
        for (startX, startY, endX, endY) in rects:
            cv2.rectangle(test_img, (startX, startY), (startX+endX, startY+endY), (0, 255, 0), 2)
        
        print('Faces found: ', len(rects))
        cv2.imwrite('C:/face_recog/test/hello.png',test_img)
        #test_im.save('C:/face_recog/test/hello.png')
    return "Successful" 

@app.route('/')
def home_1():
	return render_template('home.html')

@app.route('/uploadimg')
def uploadimg():
	return render_template('upload.html')

@app.route('/store', methods=['POST','GET'])
def store():
    if request.method == 'POST':
        f = request.files['img']  
        fileUrl = os.path.join(app.config['UPLOAD_FOLDER'],f.filename)
        f.save(fileUrl)
        print(fileUrl + "   hello my upload path=============")
        ig = f.filename
        return render_template('display_1.html', name = fileUrl)    

if __name__ == '__main__':
   app.run(debug = True, host = '0.0.0.0')