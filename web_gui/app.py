from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO
from pynput import keyboard, mouse
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app, async_mode="threading")

# store captured events in memory
captured_events = []

def capture_events(duration=3):
    """Capture keyboard and mouse events for a short duration."""
    captured_events.clear()

    def on_press(key):
        event = ("key_press", str(key))
        captured_events.append(event)
        socketio.emit("event", event)

    def on_release(key):
        event = ("key_release", str(key))
        captured_events.append(event)
        socketio.emit("event", event)

    def on_move(x, y):
        event = ("mouse_move", x, y)
        captured_events.append(event)
        socketio.emit("event", event)

    def on_click(x, y, button, pressed):
        event = ("mouse_click", x, y, str(button), pressed)
        captured_events.append(event)
        socketio.emit("event", event)

    def on_scroll(x, y, dx, dy):
        event = ("mouse_scroll", x, y, dx, dy)
        captured_events.append(event)
        socketio.emit("event", event)

    k_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    m_listener = mouse.Listener(
        on_move=on_move, on_click=on_click, on_scroll=on_scroll
    )
    k_listener.start()
    m_listener.start()
    time.sleep(duration)
    k_listener.stop()
    m_listener.stop()
    socketio.emit("capture_complete", captured_events)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/capture", methods=["POST"])
def capture():
    duration = float(request.form.get("duration", 3))
    thread = threading.Thread(target=capture_events, args=(duration,))
    thread.start()
    thread.join()
    return jsonify(captured_events)

@socketio.on("start_capture")
def handle_start_capture(data):
    duration = float(data.get("duration", 3))
    thread = threading.Thread(target=capture_events, args=(duration,))
    thread.start()

if __name__ == "__main__":
    socketio.run(app, debug=True)
