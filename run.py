# run.py

import argparse
import cv2
from datetime import datetime
import os
from insightface.app import FaceAnalysis
import numpy as np

SIMILARITY_THRESHOLD = 0.5
FRAME_SKIP = 3  # Adjust based on your system's power

def cosine_similarity(emb1, emb2):
    return np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))

def get_face_embedding(app, image_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")
    
    img = cv2.imread(image_path)
    faces = app.get(img)

    if not faces:
        raise ValueError("No face detected in reference image")

    return faces[0].embedding

def start_webcam_face_recognition(reference_embedding, app):
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Use DirectShow for better Windows performance

    # Set camera resolution to 640x480 for better speed (optional tweak)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # Reduce buffering
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    if not cap.isOpened():
        raise RuntimeError("[ERROR] Webcam could not be accessed.")

    print("[INFO] Webcam activated. Press 'q' to quit.")
    
    frame_count = 0
    detected_once = False

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[WARNING] Frame not received.")
            continue

        if frame_count % FRAME_SKIP == 0:
            faces = app.get(frame)
            for face in faces:
                embedding = face.embedding
                similarity = cosine_similarity(reference_embedding, embedding)
                x1, y1, x2, y2 = map(int, face.bbox)

                if similarity > SIMILARITY_THRESHOLD:
                    label = f"Match: {similarity:.2f}"
                    color = (0, 255, 0)
                    if not detected_once:
                        detected_once = True
                        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                        output_path = f"detected_frame_{timestamp}.jpg"
                        cv2.imwrite(output_path, frame)
                        print(f"[DETECTED] Person matched at {timestamp}")
                        print(f"[INFO] Detection frame saved: {output_path}")
                else:
                    label = f"No Match: {similarity:.2f}"
                    color = (0, 0, 255)

                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, label, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        cv2.imshow("Live Face Recognition", frame)
        frame_count += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("[INFO] Exiting video stream...")
            break

    cap.release()
    cv2.destroyAllWindows()

def main():
    parser = argparse.ArgumentParser(description="Real-time Face Recognition")
    parser.add_argument('--image', type=str, required=True, help="Path to input image")
    args = parser.parse_args()

    try:
        print("[INFO] Initializing face recognition system...")
        app = FaceAnalysis(providers=['CPUExecutionProvider'])
        app.prepare(ctx_id=-1, det_size=(320, 320))  # Smaller input size = faster inference

        print(f"[INFO] Loading reference image: {args.image}")
        reference_embedding = get_face_embedding(app, args.image)
        print("[SUCCESS] Reference face loaded. Starting recognition...")

        start_webcam_face_recognition(reference_embedding, app)

    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    main()
