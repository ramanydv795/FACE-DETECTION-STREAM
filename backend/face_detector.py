import mediapipe as mp
import numpy as np
from PIL import Image
import io

mp_face_detection = mp.solutions.face_detection

class FaceDetector:
    def __init__(self):
        self.detector = mp_face_detection.FaceDetection(
            model_selection=0,
            min_detection_confidence=0.5
        )

    def detect_and_draw(self, frame_bytes: bytes):
        # Convert bytes to numpy array
        image = Image.open(io.BytesIO(frame_bytes)).convert("RGB")
        frame = np.array(image)
        
        # Detect faces
        results = self.detector.process(frame)
        roi_list = []

        if results.detections:
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                h, w = frame.shape[:2]
                
                x = int(bboxC.xmin * w)
                y = int(bboxC.ymin * h)
                bw = int(bboxC.width * w)
                bh = int(bboxC.height * h)
                
                # Draw ROI using NumPy (NO OpenCV!)
                thickness = 3
                color = [0, 255, 0]
                
                # Top line
                frame[y:y+thickness, x:x+bw] = color
                # Bottom line
                frame[y+bh:y+bh+thickness, x:x+bw] = color
                # Left line
                frame[y:y+bh, x:x+thickness] = color
                # Right line
                frame[y:y+bh, x+bw:x+bw+thickness] = color
                
                roi_list.append({
                    "x": bboxC.xmin,
                    "y": bboxC.ymin,
                    "width": bboxC.width,
                    "height": bboxC.height,
                    "confidence": detection.score[0]
                })

        # Convert back to bytes
        output_image = Image.fromarray(frame)
        output_bytes = io.BytesIO()
        output_image.save(output_bytes, format="JPEG")
        return output_bytes.getvalue(), roi_list