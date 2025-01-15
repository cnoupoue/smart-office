import os
import io
import picamera
import logging
import socketserver
from threading import Condition, Thread
from http import server
import json
import controllers.mqtt_controller as mqtt_controller
import controllers.common as common
import env
import time
import utils.ip as ip

def _get_page():
    return """\
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Raspberry Pi - Surveillance Camera</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f9;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                text-align: center;
            }
            h1 {
                color: #333;
                font-size: 2.5em;
                margin-bottom: 20px;
            }
            .camera-container {
                background-color: #fff;
                border-radius: 15px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                padding: 20px;
                max-width: 700px;
                width: 100%;
            }
            img {
                width: 100%;
                max-width: 640px;
                min-width: 640px;
                min-height: 480px;
                // height: auto;
                border: grey 5px solid;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
                display: none;
            }
            .footer {
                position: fixed;
                bottom: 10px;
                width: 100%;
                text-align: center;
                color: #aaa;
                font-size: 1em;
            }
            .status {
                margin-top: 20px;
                font-size: 1.2em;
                color: #555;
            }
            .button {
                padding: 10px 20px;
                font-size: 1em;
                cursor: pointer;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                margin-top: 10px;
            }
        </style>
        <script>
            function toggleCamera() {
                fetch('/camera/toggle', { method: 'POST' })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error(`HTTP error! status: ${response.status}`);
                        }
                        return response.json();
                    })
                    .then(data => {
                        if (data.status === 'started') {
                            document.getElementById("camera-status").innerText = "Camera allumée";
                            document.getElementById("camera-image").src = "stream.mjpg";
                            document.getElementById("camera-image").style.display = "inline";
                        } else {
                            document.getElementById("camera-status").innerText = "Camera éteinte";
                            document.getElementById("camera-image").style.display = "none";
                            document.getElementById("camera-image").src = "";
                        }
                    })
                    .catch(error => console.error('Error toggling camera:', error));
            }

            function checkCameraStatus() {
                fetch('/camera/status', { method: 'POST' })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error(`HTTP error! status: ${response.status}`);
                        }
                        return response.json();
                    })
                    .then(data => {
                        if (data.status === 'started') {
                            document.getElementById("camera-status").innerText = "Camera allumée";
                            document.getElementById("camera-image").src = "stream.mjpg";
                            document.getElementById("camera-image").style.display = "inline";
                        } else {
                            document.getElementById("camera-status").innerText = "Camera éteinte";
                            document.getElementById("camera-image").style.display = "none";
                            document.getElementById("camera-image").src = "";
                        }
                    })
                    .catch(error => console.error('Error checking camera status:', error));
            }

            window.onload = () => setTimeout(() => { checkCameraStatus(); }, 2000);
        </script>
    </head>
    <body>
        <div class="camera-container">
            <h1> Caméra du local: """ + str(common.get_premise()) + """ </h1>
            <img id="camera-image" src="" alt="Surveillance Camera Stream">
            <p id="camera-status" class="status">Camera éteinte</p>
            <button class="button" onclick="toggleCamera()">Démarrer/Stopper la Camera</button>
        </div>
    </body>
    </html>
    """

camera = None
output = None

class _StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class _StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        global output, camera
        if self.path == '/camera':
            content = _get_page().encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

    def do_POST(self):
        global camera_active
        if self.path == '/camera/toggle':
            if camera_active:
                print("Camera stopped")
                camera.stop_recording()
                camera_active = False
            else:
                camera.start_recording(output, format='mjpeg')
                print("Camera started")
                camera_active = True
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {"status": "started" if camera_active else "stopped"}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        elif self.path == '/camera/status':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {"status": "started" if camera_active else "stopped"}
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
class _StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

camera_active = False

def camera_hello():
    while True:
        mqtt_controller.put_in_publish_queue(env.CAMERA, json.dumps({"ip": ip.read(), "status": camera_active}))
        time.sleep(env.CAMERA_HELLO_DELAY)

def run():
    global output, camera
    with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
        output = _StreamingOutput()
        Thread(target=camera_hello, daemon=True).start()
        try:
            address = ('', 8000)
            server = _StreamingServer(address, _StreamingHandler)
            print("Server started...")
            server.serve_forever()
        finally:
            if camera_active:
                camera.stop_recording()
                print("camera stopped")
            camera.close()