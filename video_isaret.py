from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import cv2
import numpy as np
import pickle

app = Flask(__name__)
socketio = SocketIO(app)

cap = cv2.VideoCapture("video.mp4")

def check(frame1):
    space_counter = 0
    for pos in liste:
        x, y = pos

        crop = frame1[y:y+15, x:x+26]
        count = cv2.countNonZero(crop)

        if count <= 150:
            space_counter += 1

    percentage = int(100 - (space_counter / len(liste)) * 100)

    return percentage

@app.route('/')
def index():
    return render_template('index_ajax.html')

@app.route('/get_percentage', methods=['GET'])
def get_percentage():
    _, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 1)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    median = cv2.medianBlur(thresh, 5)
    dilates = cv2.dilate(median, np.ones((3, 3)), iterations=1)

    percentage = check(dilates)

    

    return jsonify({'percentage': percentage, 'image_url': '/static/video_frame.jpg'})

if __name__ == '__main__':
    with open("noktalar", "rb") as f:
        liste = pickle.load(f)

    socketio.run(app, debug=True, port=5001)
