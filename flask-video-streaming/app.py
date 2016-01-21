#!/usr/bin/env python
from flask import (
        Flask, 
        render_template, 
        Response,
        send_file,
)

# Raspberry Pi camera module (requires picamera package)
from camera_pi import Camera
import tempfile
from datetime import datetime
import os, sys, re

app = Flask(__name__)
path = os.path.dirname(os.path.realpath(__file__))
app._static_folder = path + '/static'


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/img.jpg')
def get_jpg():
    """
    #with tempfile.TemporaryFile() as tf:
    import picamera
    with picamera.camera as c:
        timestamp = datetime.now().isoformat()
        #photo_path = '%s/static/photos/%s.jpg' % (path, timestamp)
        photo_path = '%s/static/img.jpg' % (path)
        c.hflip = c.vflip = False
        c.resolution = (640, 400)
        c.capture(photo_path)
        #tf.seek(0)
        #return send_file(tf, mimetype='image/jpeg')
        return app.send_static_file('img.jpg')
    """
    frame = Camera().get_frame()
    static_path = '/static/img.jpg'
    photo_path = path + static_path
    with open(photo_path, 'wb') as tf:
        tf.write(frame)
        tf.seek(0)
        return send_file(photo_path, mimetype='image/jpeg')
        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
