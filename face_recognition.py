import os
import cv2
import numpy as np
from insightface.app import FaceAnalysis
import onnxruntime as ort

# === CONFIG ===
REFERENCE_IMAGE = "input/sample_input.jpg"  # Make sure the path is correct relative to your script
SIMILARITY_THRESHOLD = 0.6

def check_onnx_providers():
    providers = ort.get_available_providers()
    print(f"[INFO] Available ONNX Providers: {providers}")
    print("[ACTION] Forcing CPU execution...")

def initialize_face_analysis():
    app = FaceAnalysis(providers=['CPUExecutionProvider'])
    app.prepare(ctx_id=-1, det_size=(640, 640))
    return app

def get_face_embedding(app, image_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")
    
    img = cv2.imread(image_path)
    faces = app.get(img)
    
    if not faces:
        raise ValueError("No face detected in reference image")

    return faces[0].embedding

def cosine_similarity(emb1, emb2):
    return np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))

def start_face_recognition(app, reference_embedding):
    cap = cv2.VideoCapture(0)  # Change index if necessary

    if not cap.isOpened():
        raise RuntimeError("Webcam not accessible")

    print("[INFO] Webcam activated. Press 'q' to exit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[WARNING] Could not grab frame.")
            continue

        faces = app.get(frame)
        for face in faces:
            embedding = face.embedding
            similarity = cosine_similarity(reference_embedding, embedding)

            x1, y1, x2, y2 = map(int, face.bbox)

            if similarity > SIMILARITY_THRESHOLD:
                label = f"Match: {similarity:.2f}"
                color = (0, 255, 0)
            else:
                label = f"No Match: {similarity:.2f}"
                color = (0, 0, 255)

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        cv2.imshow("Face Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("[INFO] Exiting webcam...")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    try:
        check_onnx_providers()
        app = initialize_face_analysis()
        print("[INFO] Processing reference image...")
        ref_embedding = get_face_embedding(app, REFERENCE_IMAGE)
        print("[SUCCESS] Reference face encoded. Starting recognition...")
        start_face_recognition(app, ref_embedding)
    except Exception as e:
        print(f"[ERROR] {e}")
