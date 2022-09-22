# import os
# from pymongo import MongoClient
# import numpy as np
# import cv2
#
#
# def finger():
#     sample = cv2.imread("C:/Users/rajra/Downloads/papa.bmp")
#
#     best_score = 0
#     filename = None
#     image = None
#     kp1, kp2, mp = None, None, None
#     i = 0
#     # client = MongoClient("mongodb+srv://kartik:aadhar_data@cluster0.6nbl1l4.mongodb.net/?retryWrites=true&w=majority")
#     # db = client["aadharDB"]
#     # finger_data = db["fingerDB"]
#     # files = finger_data.find({})
#     for file in files:
#         print(i)
#         i=i+1
#         fingerimg = np.uint8(np.array(file["finger"]))
#         # print(fingerimg.dtype)
#         # print(sample.dtype)
#         fingerprint_image=cv2.cvtColor(fingerimg, cv2.COLOR_BGR2GRAY)
#         # print(sample)
#         sift = cv2.SIFT_create()
#
#         keypoints_1, descriptors_1 = sift.detectAndCompute(sample, None)
#         keypoints_2, descriptors_2 = sift.detectAndCompute(fingerprint_image, None)
#
#         matches = cv2.FlannBasedMatcher({'algorithm': 1, 'trees': 10},
#                                         {}).knnMatch(descriptors_1, descriptors_2, k=2)
#
#         match_points = []
#
#         for p, q in matches:
#             if p.distance < 0.1 * q.distance:
#                 match_points.append(p)
#
#         keypoints = 0
#         if len(keypoints_1) < len(keypoints_2):
#             keypoints = len(keypoints_1)
#         else:
#             keypoints = len(keypoints_2)
#
#         if len(match_points) / keypoints * 100 > best_score:
#             best_score = len(match_points) / keypoints * 100
#             filename = file["Aadhar"]
#             image = fingerprint_image
#             kp1, kp2, mp = keypoints_1, keypoints_2, match_points
#         # break
#
#     print(f"BEST MATCH:   {filename}")
#     print("SCORE: " + str(best_score))
#
#     result = cv2.drawMatches(sample, kp1, image, kp2, mp, None)
#     result = cv2.resize(result, None, fx=1, fy=1)
#     cv2.imshow("Result", result)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
#     return filename
import os

import cv2
def finger():
    sample = cv2.imread("C:/Users/rajra/PycharmProjects/sih/static/fingerprint.bmp")

    best_score = 0
    filename = None
    image = None
    kp1, kp2, mp = None, None, None
    for file in [file for file in os.listdir("C:/Users/rajra/PycharmProjects/sih/fingerdata")]:
        fingerprint_image = cv2.imread("C:/Users/rajra/PycharmProjects/sih/fingerdata/" + file)
        sift = cv2.SIFT_create()

        keypoints_1, descriptors_1 = sift.detectAndCompute(sample, None)
        keypoints_2, descriptors_2 = sift.detectAndCompute(fingerprint_image, None)

        matches = cv2.FlannBasedMatcher({'algorithm': 1, 'trees': 10},
                                        {}).knnMatch(descriptors_1, descriptors_2, k=2)

        match_points = []

        for p, q in matches:
            if p.distance < 0.1 * q.distance:
                match_points.append(p)

        keypoints = 0
        if len(keypoints_1) < len(keypoints_2):
            keypoints = len(keypoints_1)
        else:
            keypoints = len(keypoints_2)

        if len(match_points) / keypoints * 100 > best_score:
            best_score = len(match_points) / keypoints * 100
            filename = file
            image = fingerprint_image
            kp1, kp2, mp = keypoints_1, keypoints_2, match_points

    print("BEST MATCH: " + filename)
    print("SCORE: " + str(best_score))


    return filename