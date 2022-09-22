import cv2
from source.simple_facerec import SimpleFacerec
import win32gui
import re


def face():
    # Encode faces from a folder
    sfr = SimpleFacerec()
    # sfr.load_encoding_images("source/images/")
    # sfr.add_data()
    try:
    # Load Camera
        cap = cv2.VideoCapture(0)
        sfr.add_to_arr()

        while True:
            ret, frame = cap.read()

            # Detect Faces
            face_locations, face_names = sfr.detect_known_faces(frame)
            for face_loc, name in zip(face_locations, face_names):
                if name != 'Unknown':
                    # print(name)
                    return name
                y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
                cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)

            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1)
            cv2.setWindowProperty("Frame", cv2.WND_PROP_TOPMOST, 1)
            if key == 27:
                break
    except ValueError:
        return "encoding images not found"
    finally:
        cap.release()
        cv2.destroyAllWindows()

