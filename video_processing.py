# scr/video_processing.py

import cv2
import torch
import time
from datetime import datetime
from scr.face_detection import FaceDetector
from scr.face_recognition import FaceRecognizer

# Set confidence threshold for cosine similarity (lower = stricter)
SIMILARITY_THRESHOLD = 0.45

def start_video_stream(input_image_path):
    # Initialize Face Detector & Recognizer
    detector = FaceDetector()
    recognizer = FaceRecognizer()

    print("[INFO] Extracting embedding from input image...")
    input_embedding = recognizer.extract_embedding(input_image_path)
    if input_embedding is None:
        print("[ERROR] No face detected in input image!")
        return

    # Initialize video capture from webcam (0 = default laptop cam)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERROR] Webcam not accessible!")
        return

    print("[INFO] Webcam stream started successfully.")
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Frame not received from webcam.")
            break

        frame_count += 1
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect faces
        faces, boxes = detector.detect_faces(rgb_frame)

        for i, face in enumerate(faces):
            emb = recognizer.get_embedding(face)
            if emb is not None:
                similarity = recognizer.compare_embeddings(input_embedding, emb)
                if similarity < SIMILARITY_THRESHOLD:
                    # Draw bounding box & label
                    x1, y1, x2, y2 = map(int, boxes[i])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, f"Matched ({similarity:.2f})", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                    # Log timestamp
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(f"[DETECTED] Person matched at {timestamp} (Frame: {frame_count})")

                    # Save frame
                    cv2.imwrite(f"detection_{frame_count}.jpg", frame)
                    with open("detections_log.txt", "a") as log_file:
                        log_file.write(f"Matched at {timestamp} - Frame {frame_count}\n")

        # Show the frame
        cv2.imshow("Live CCTV (Laptop Webcam)", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release everything
    cap.release()
    cv2.destroyAllWindows()
