import face_recognition
import cv2
import os
import glob
import numpy as np
from pymongo import MongoClient

client = MongoClient("mongodb+srv://kartik:aadhar_data@cluster0.6nbl1l4.mongodb.net/?retryWrites=true&w=majority")
db = client["aadharDB"]
# aadharDB = db["aadhar_data"]
encodings_data_mon = db["encoded_data"]


class SimpleFacerec:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.known_face_names_data = []
        self.known_face_encodings_data = []
        # Resize frame for a faster speed
        self.frame_resizing = 0.25

    def load_encoding_images(self, images_path):
        """
        Load encoding images from path
        :param images_path:
        :return:
        """
        # Load Images
        images_path = glob.glob(os.path.join(images_path, "*.*"))
        print("{} encoding images found.".format(len(images_path)))
        # Store image encoding and names
        for img_path in images_path:
            img = cv2.imread(img_path)
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Get the filename only from the initial file path.
            basename = os.path.basename(img_path)
            (filename, ext) = os.path.splitext(basename)
            # Get encoding
            img_encoding = face_recognition.face_encodings(rgb_img)[0]

            # Store file name and file encoding
            self.known_face_encodings.append(img_encoding)
            self.known_face_names.append(filename)
        print("Encoding images loaded")

    def add_data(self):
        self.load_encoding_images("source/images")
        i = 0
        for user in self.known_face_encodings:
            res = user.tolist()
            data = {
                "img_encode": res,
                "img_name": self.known_face_names[i]
            }
            i += 1
            encodings_data_mon.insert_one(data)

    def add_to_arr(self):
        all_data = encodings_data_mon.find({})
        # print(all_data)
        for data in all_data:
            # print(data["img_name"])
            self.known_face_names_data.append(data["img_name"])
            self.known_face_encodings_data.append(np.array(data["img_encode"]))

    def detect_known_faces(self, frame):

        small_frame = cv2.resize(frame, (0, 0), fx=self.frame_resizing, fy=self.frame_resizing)
        # Find all the faces and face encodings in the current frame of video
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.known_face_encodings_data, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(self.known_face_encodings_data, face_encoding)
            best_match_index = np.argmin(face_distances)
            # print(type(self.known_face_names_data[best_match_index]))
            if matches[best_match_index]:
                # print(type(face_distances[best_match_index]))
                if face_distances[best_match_index] < 0.4:
                    name = self.known_face_names_data[best_match_index]
            face_names.append(name)

        # Convert to numpy array to adjust coordinates with frame resizing quickly
        face_locations = np.array(face_locations)
        face_locations = face_locations / self.frame_resizing
        return face_locations.astype(int), face_names
