from fastapi import FastAPI, WebSocket, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import asyncio
import json
import structlog
from database import get_db, create_tables, ROIData
from face_detector import FaceDetector

logger = structlog.get_logger()
app = FastAPI(title="Face Detection Stream")
detector = FaceDetector()
frame_queue = asyncio.Queue(maxsize=10)
latest_roi = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    create_tables()
    logger.info("Database tables created")

# Endpoint 1 — Receive video feed
@app.websocket("/ws/feed")
async def receive_feed(websocket: WebSocket):
    await websocket.accept()
    logger.info("Video feed connected")
    try:
        while True:
            frame_bytes = await websocket.receive_bytes()
            if not frame_queue.full():
                await frame_queue.put(frame_bytes)
    except Exception as e:
        logger.error("Feed error", error=str(e))

# Endpoint 2 — Serve processed video
@app.websocket("/ws/stream")
async def stream_feed(websocket: WebSocket, db: Session = Depends(get_db)):
    global latest_roi
    await websocket.accept()
    logger.info("Stream client connected")
    try:
        while True:
            if not frame_queue.empty():
                frame_bytes = await frame_queue.get()
                processed_frame, roi_list = detector.detect_and_draw(frame_bytes)
                
                # Save ROI to DB
                if roi_list:
                    latest_roi = roi_list
                    for roi in roi_list:
                        db_roi = ROIData(**roi)
                        db.add(db_roi)
                    db.commit()
                
                await websocket.send_bytes(processed_frame)
            else:
                await asyncio.sleep(0.01)
    except Exception as e:
        logger.error("Stream error", error=str(e))

# Endpoint 3 — Serve ROI data
@app.get("/roi")
async def get_roi(db: Session = Depends(get_db)):
    rois = db.query(ROIData).order_by(ROIData.timestamp.desc()).limit(10).all()
    return {"roi_data": [
        {
            "id": r.id,
            "x": r.x, "y": r.y,
            "width": r.width,
            "height": r.height,
            "confidence": r.confidence,
            "timestamp": str(r.timestamp)
        } for r in rois
    ]}

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)