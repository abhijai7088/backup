import cv2

def find_working_camera():
    for i in range(5):
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)  # Use DirectShow backend
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print(f"✅ Found working camera at index {i}")
                return cap
        cap.release()
    return None

cap = find_working_camera()

if cap:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("SplitCam Live Feed", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
else:
    print("❌ No working camera found.")
