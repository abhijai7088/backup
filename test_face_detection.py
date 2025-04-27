# scr/test_face_detection.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scr.face_detection import FaceDetector
import cv2

detector = FaceDetector()

cap = cv2.VideoCapture(0) # 0 = Default laptop webcam

print("[INFO] Starting webcam... Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    detections = detector.detect_faces(frame)

    for box, _ in detections:
        x1, y1, x2, y2 = [int(b) for b in box]
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    cv2.imshow("Face Detection Test", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
