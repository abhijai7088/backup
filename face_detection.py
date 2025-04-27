# scr/face_detection.py

from facenet_pytorch import MTCNN
import cv2
import numpy as np
from PIL import Image
import torch

class FaceDetector:
    def __init__(self, device=None):
        self.device = device if device else ('cuda' if torch.cuda.is_available() else 'cpu')
        self.mtcnn = MTCNN(keep_all=True, device=self.device)

    def detect_faces(self, frame):
        """
        Detects all faces in a given image frame using MTCNN.

        Args:
            frame (np.array): Image frame (from webcam or image file)

        Returns:
            boxes (List of tuples): Bounding boxes for detected faces
            faces (List of PIL.Image): Cropped face images
        """
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        boxes, _ = self.mtcnn.detect(img)
        faces = []

        if boxes is not None:
            for box in boxes:
                x1, y1, x2, y2 = [int(b) for b in box]
                face = frame[y1:y2, x1:x2]
                face_pil = Image.fromarray(cv2.cvtColor(face, cv2.COLOR_BGR2RGB))
                faces.append((box, face_pil))
        
        return faces  # List of (box, face image)
