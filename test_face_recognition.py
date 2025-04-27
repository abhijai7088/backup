import unittest
import cv2
import os
import torch
import numpy as np
from face_recognition import FaceRecognizer

class TestFaceRecognition(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialize FaceRecognizer before running tests"""
        cls.model_path = "models/arcface_resnet100.pth"
        cls.recognizer = FaceRecognizer(model_path=cls.model_path)
        cls.input_image_path = "input/person.jpg"

    def test_1_model_file_exists(self):
        """Check if ArcFace model file exists"""
        self.assertTrue(os.path.exists(self.model_path), "[ERROR] Model file not found!")

    def test_2_load_face_recognition_model(self):
        """Check if the ArcFace model loads correctly"""
        self.assertIsNotNone(self.recognizer.recognition_model, "[ERROR] ArcFace Model failed to load!")

    def test_3_webcam_accessibility(self):
        """Test if the laptop webcam opens successfully"""
        cap = cv2.VideoCapture(0)
        ret, _ = cap.read()
        cap.release()
        self.assertTrue(ret, "[ERROR] Unable to access the webcam!")

    def test_4_face_embedding_extraction(self):
        """Test if the system can extract a face embedding from the input image"""
        input_img = cv2.imread(self.input_image_path)
        self.assertIsNotNone(input_img, "[ERROR] Input image not found!")
        
        embedding = self.recognizer.extract_face_embedding(input_img)
        self.assertIsNotNone(embedding, "[ERROR] Failed to extract face embedding!")

    def test_5_real_time_face_recognition(self):
        """Test if the system detects and recognizes a face from the webcam"""
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()

        self.assertTrue(ret, "[ERROR] Failed to capture a frame from webcam!")

        detected_embedding = self.recognizer.extract_face_embedding(frame)
        self.assertIsNotNone(detected_embedding, "[ERROR] No face detected in webcam frame!")

if __name__ == "__main__":
    unittest.main()
