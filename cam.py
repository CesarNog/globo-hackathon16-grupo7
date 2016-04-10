#!/usr/bin/python
from flask import Flask, render_template, Response

from camera import VideoCamera

app = Flask(__name__)


@app.route("/")
def main():
    # Create a template data dictionary to send any data to the template
    templateData = {
        'title': 'LiveCam'
    }
    # Pass the template data into the template livecam.html and return it to the user
    return render_template('livecam.html', **templateData)


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(host='192.168.0.225', debug=True)
