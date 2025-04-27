import cv2
from ultralytics import YOLO
import datetime

# Load YOLOv8 model (make sure this is YOLOv8 compatible)
model_path = r"models/object_recognition/yolov8n.pt"  # or your own YOLOv8-trained model
model = YOLO(model_path)

# Open webcam (change to your IP camera if needed)
cap = cv2.VideoCapture(0)  # 0 for default webcam

# Input image to match against
input_img_path = r"input_images/person.jpg"  # Update path as needed
input_img = cv2.imread(input_img_path)

# Run loop
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLO detection
    results = model(frame)[0]

    for box in results.boxes:
        conf = box.conf[0]
        cls = int(box.cls[0])
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        label = model.names[cls]

        # Confidence filter
        if conf > 0.5:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Optional: Save frame and log timestamp
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[INFO] Detected {label} at {timestamp}")
            cv2.imwrite(f"detections/detected_{timestamp}.jpg", frame)

    cv2.imshow("Live Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
