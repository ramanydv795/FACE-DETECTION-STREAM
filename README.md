# 🎯 Real-Time Face Detection Streaming System

A production-style real-time face detection system built using FastAPI, React, WebSockets, MediaPipe, NumPy, PostgreSQL, JWT Authentication, Docker, and async streaming architecture.

This project accepts a live webcam feed from the browser, performs AI-based face detection in real-time, draws ROI bounding boxes without OpenCV, stores ROI metadata in PostgreSQL, and streams processed frames back to the frontend.

---

# 🚀 Features

* 📹 Real-time webcam streaming
* ⚡ WebSocket-based low-latency communication
* 🧠 MediaPipe AI face detection
* 📦 NumPy-based ROI drawing (without OpenCV)
* 🗄️ PostgreSQL ROI metadata storage
* 🔐 JWT Authentication
* 🧪 Integration testing with Pytest
* 🐳 Dockerized architecture
* 📊 FPS monitoring dashboard
* 🔄 Async producer-consumer streaming pipeline
* 🌐 React frontend with live ROI telemetry
* 📈 Structured backend architecture

---

# 🏗️ Architecture

![Architecture](architecture.png)

## Data Flow

```text
Browser Webcam
      ↓
WebSocket /ws/feed
      ↓
FastAPI Backend
      ↓
asyncio.Queue
      ↓
MediaPipe Face Detection
      ↓
NumPy ROI Drawing
      ↓
PostgreSQL Storage
      ↓
WebSocket /ws/stream
      ↓
React Frontend Dashboard
```

---

# 🛠️ Tech Stack

## Frontend

* React.js
* HTML5 Canvas
* WebSockets
* Browser MediaDevices API

## Backend

* FastAPI
* Python 3.11
* AsyncIO
* SQLAlchemy
* JWT Authentication

## AI / Computer Vision

* MediaPipe Face Detection
* NumPy
* Pillow

## Database

* PostgreSQL

## DevOps

* Docker
* Docker Compose

## Testing

* Pytest
* FastAPI TestClient

---

# ⚙️ System Design Decisions

## Why WebSockets?

Traditional REST polling introduces latency and unnecessary HTTP overhead.

WebSockets enable:

* Real-time bidirectional communication
* Continuous frame streaming
* Lower latency
* Better streaming performance

---

## Why MediaPipe?

MediaPipe was chosen over Haar Cascades/OpenCV because:

* Faster real-time inference
* Better detection accuracy
* Lightweight and optimized
* Works without OpenCV-based detection pipeline
* Production-grade mobile/web optimization

---

## Why NumPy ROI Drawing?

The assignment explicitly restricted OpenCV for drawing bounding boxes.

ROI rectangles are drawn directly using NumPy array slicing:

```python
frame[y:y+thickness, x:x+bw] = color
```

Benefits:

* Zero-copy memory operations
* Extremely fast pixel manipulation
* Minimal latency overhead

---

## Why PostgreSQL?

PostgreSQL was selected because ROI data is structured and relational.

Stored metadata:

* ROI coordinates
* Detection confidence
* Timestamp

Advantages:

* ACID compliance
* Better schema structure
* Efficient querying
* Production scalability

---

# 📂 Project Structure

```text
face-detection-stream/
│
├── backend/
│   ├── main.py
│   ├── auth.py
│   ├── database.py
│   ├── face_detector.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── tests/
│       ├── __init__.py
│       └── test_main.py
│
├── frontend/
│   ├── src/
│   │   └── App.js
│   ├── package.json
│   └── Dockerfile
│
├── architecture.png
├── AI_REPORT.md
├── docker-compose.yml
└── README.md
```

---

# 🔐 Authentication

JWT authentication is implemented for secure API access.

## Flow

1. Frontend requests token from `/token`
2. Backend generates JWT token
3. Frontend stores token in state
4. Protected endpoints require Bearer token
5. Backend validates token before serving data

---

# 📡 API Endpoints

## Generate JWT Token

```http
GET /token
```

Returns:

```json
{
  "access_token": "jwt-token",
  "token_type": "bearer"
}
```

---

## Send Webcam Frames

```http
WS /ws/feed
```

Accepts binary JPEG frame stream from browser.

---

## Receive Processed Frames

```http
WS /ws/stream
```

Streams processed frames with ROI overlays.

---

## Get ROI Metadata

```http
GET /roi
```

Protected with JWT authentication.

Returns latest face detection ROI data.

---

## Health Check

```http
GET /health
```

Returns API health status.

---

# ⚡ Async Streaming Architecture

The backend uses a producer-consumer architecture with `asyncio.Queue`.

## Producer

`/ws/feed`

* receives raw video frames
* pushes frames into queue

## Consumer

`/ws/stream`

* pulls frames from queue
* performs AI inference
* draws ROI
* stores ROI metadata
* streams processed frames back

Benefits:

* prevents blocking
* improves scalability
* separates streaming from inference
* smoother real-time processing

---

# 🧪 Testing

Integration tests were implemented using Pytest and FastAPI TestClient.

## Test Coverage

* Root endpoint
* Health endpoint
* JWT token generation
* Protected route authentication
* Invalid token handling
* ROI endpoint access
* JWT verification logic

## Run Tests

```bash
pytest
```

---

# 🐳 Docker Setup

The project is fully containerized.

## Services

* Backend (FastAPI)
* Frontend (React)
* PostgreSQL
* Adminer

## Run Entire Stack

```bash
docker-compose up --build
```

---

# 🚀 Local Development Setup

## 1. Clone Repository

```bash
git clone https://github.com/ramanydv795/FACE-DETECTION-STREAM.git
```

---

## 2. Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Backend runs on:

```text
http://localhost:8000
```

---

## 3. Frontend Setup

```bash
cd frontend
npm install
npm start
```

Frontend runs on:

```text
http://localhost:3000
```

---

# 📊 Frontend Dashboard Features

* Live processed video stream
* FPS monitoring
* JWT authentication status
* ROI telemetry panel
* Confidence visualization
* Real-time detection updates
* Architecture information panel

---

# 🧠 Challenges Faced

## Challenge 1 — Drawing ROI Without OpenCV

Solved using direct NumPy pixel manipulation.

---

## Challenge 2 — Real-Time Streaming

Solved using WebSockets and async producer-consumer architecture.

---

## Challenge 3 — Synchronizing Frontend and Backend

Solved using binary WebSocket frame streaming and React canvas rendering.

---

# 🔮 Future Improvements

Potential future enhancements:

* Multi-face support
* WebRTC streaming
* Prometheus metrics
* Rate limiting
* Kubernetes deployment
* GPU acceleration
* Face recognition
* Object detection support
* Redis-based distributed queues
* Cloud deployment

---

# 📈 Performance Considerations

Optimizations implemented:

* AsyncIO non-blocking architecture
* Queue-based frame buffering
* NumPy zero-copy ROI drawing
* JPEG compression for streaming
* Lightweight MediaPipe inference

---

# 🤖 AI Collaboration Report

AI tools were used for:

* Architecture brainstorming
* NumPy optimization ideas
* Async queue pattern guidance
* Documentation structure
* Docker optimization suggestions

All implementation decisions, debugging, integration, and system understanding were performed manually.

---

# 📚 Key Learnings

Through this project I learned:

* Real-time streaming systems
* WebSocket architecture
* Async backend programming
* JWT authentication
* AI inference pipelines
* Docker containerization
* Integration testing
* Production-style system design

---

# 🙌 Acknowledgements

Libraries and tools used:

* FastAPI
* React.js
* MediaPipe
* NumPy
* PostgreSQL
* Docker
* SQLAlchemy
* Pytest

---

# 👨‍💻 Author

Raman Yadav

GitHub:

```text
https://github.com/ramanydv795
```

---

# ⭐ Final Note

This project was designed to simulate a production-style AI streaming system while keeping the architecture understandable, scalable, and recruiter-friendly.

The goal was not only to build a working prototype, but also to demonstrate engineering thinking, async system design, and full-stack AI integration.
