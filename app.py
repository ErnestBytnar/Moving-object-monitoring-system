from flask import Flask, render_template, redirect, url_for, Response, send_from_directory
from picamera import PiCamera
from picamera.array import PiRGBArray
from datetime import datetime
import os
import threading
import time
import cv2
import pigpio

app = Flask(__name__)


camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 64
recording = False
recording_start_time = None
segment_counter = 1
segment_interval = 30

RECORDINGS_FOLDER = "recordings"
os.makedirs(RECORDINGS_FOLDER, exist_ok=True)


servo_pin = 25
left_sensor = 22
center_sensor = 27
right_sensor = 17

pi = pigpio.pi()

if not pi.connected:
    print("Błąd połączenia z pigpio")
    exit()

min_pulse_width = 500  # 1 ms
max_pulse_width = 2000  # 2 ms


def go_to_center():
    pi.set_servo_pulsewidth(servo_pin, (min_pulse_width + max_pulse_width) // 2)
    print("Serwo ustawione na środek (0°)")
    time.sleep(1)

def go_left():
    pi.set_servo_pulsewidth(servo_pin, max_pulse_width)
    print("Serwo ustawione na lewo (90°)")
    time.sleep(1)

def go_right():
    pi.set_servo_pulsewidth(servo_pin, min_pulse_width)
    print("Serwo ustawione na prawo (-90°)")
    time.sleep(1)

pi.set_mode(left_sensor, pigpio.INPUT)
pi.set_mode(center_sensor, pigpio.INPUT)
pi.set_mode(right_sensor, pigpio.INPUT)

def monitor_sensors():
    left_state = pi.read(left_sensor)
    center_state = pi.read(center_sensor)
    right_state = pi.read(right_sensor)

    if left_state == 1:
        go_left()
    elif center_state == 1:
        go_to_center()
    elif right_state == 1:
        go_right()


def add_timestamp_to_frame(frame):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    color = (255, 255, 255)
    thickness = 2
    position = (10, 30)
    cv2.putText(frame, timestamp, position, font, font_scale, color, thickness)
    return frame

last_recording_number = None


def record_video_segment():
    global recording, segment_counter
    while recording:
        timestamp = datetime.now().strftime('%Y%m%d')
        filename = os.path.join(RECORDINGS_FOLDER, f"{timestamp}_segment{segment_counter}.h264")
        camera.start_recording(filename)
        start_time = time.time()
        while recording and (time.time() - start_time < segment_interval):
            camera.wait_recording(1)
        camera.stop_recording()
        segment_counter += 1


def generate_frames():
    with PiRGBArray(camera) as stream:
        while True:
            camera.capture(stream, format="bgr")
            frame = stream.array
            frame = add_timestamp_to_frame(frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            stream.truncate(0)

# Trasy Flask
@app.route('/')
def index():
    recordings = [f for f in os.listdir(RECORDINGS_FOLDER) if f.endswith(".h264")]
    return render_template('index.html', recording=recording, recordings=recordings)

@app.route('/start')
def start():
    global recording, recording_start_time
    if not recording:
        recording = True
        recording_start_time = time.time()

        thread = threading.Thread(target=monitor_sensors_loop)
        thread.start()

        video_thread = threading.Thread(target=record_video_segment)
        video_thread.start()

    return redirect(url_for('index'))

@app.route('/stop')
def stop():
    global recording
    if recording:
        recording = False
    return redirect(url_for('index'))

@app.route('/live')
def live():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(RECORDINGS_FOLDER, filename)

def monitor_sensors_loop():
    while recording:
        monitor_sensors()
        time.sleep(0.1)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
