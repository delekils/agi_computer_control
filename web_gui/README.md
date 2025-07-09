# Web GUI

This directory contains a simple Flask application that exposes a web interface
for capturing keyboard and mouse events. It demonstrates how a browser can
interact with some of the functionality in this project.

## Usage

Install the additional requirements and run the server:

```bash
pip install Flask Flask-SocketIO pynput
python app.py
```

Open `http://localhost:5000` in your browser to capture a short sequence of HID
events.

Click the **Start Real-time Capture** button to see events streamed live using
WebSockets.
