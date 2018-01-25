# -*- coding: UTF-8 -*-
import sys, os, dlib, cv2, glob
import numpy as np
from skimage import io

shape_predictor_68_face_landmarks = "./DataModel/shape_predictor_68_face_landmarks.dat"
face_recognition_resnet_model = "./DataModel/dlib_face_recognition_resnet_model_v1.dat"
face_folder_path = "./faces"
face_model_list = []


def init_facial_model():
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(shape_predictor_68_face_landmarks)
    recognitor = dlib.face_recognition_model_v1(face_recognition_resnet_model)
    return (detector, predictor ,recognitor)

# Facial regional marker to Rect boundary information
def facialRM_to_rect(rect):
    x = rect.left()
    y = rect.top()
    w = rect.right() - x
    h = rect.bottom() - y
    return (x, y, w, h)

# Facial feature marker(shape) to Numpy array
def shape_to_np(shape, dtype = "int"):
    coords = np.zeros((68, 2), dtype = dtype)
    for i in range(0, 68):
        coords[i] = (shape.part(i).x, shape.part(i).y)
    return coords

# Resize image file
def resize(image, width = 1080):
    r = 0
    dim = None

    if image.shape[1] > width:
        r = width * 1.0 / image.shape[1]
        dim = (width, int(image.shape[0] * r))
    else:
        dim = (image.shape[1], image.shape[0])

    resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)    
    return resized

# Facial regional marker to image file
def facial_regional_marker(imagePath):
    detector, predictor ,recognitor = init_facial_model()

    image = cv2.imread(imagePath)
    image = resize(image, width = 1080)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 1)

    for (i, rect) in enumerate(rects):
        shape_predictor = predictor(gray, rect)
        shape = shape_to_np(shape_predictor)

        (x, y, w, h) = facialRM_to_rect(rect)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.putText(image,
            "Face #{}".format(i + 1),
            (x - 10, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5, (0, 255, 0), 2)
            
        for (x, y) in shape:
            cv2.circle(image, (x, y), 2, (0, 0, 255), -1)

    cv2.imshow("Output", image)
    cv2.waitKey(0)

# Facial_model_acquisition
def facial_model_acquisition():
    detector, predictor ,recognitor = init_facial_model()

    for face in glob.glob(os.path.join(face_folder_path, "*.jpg")):
        # print("Processing file: {}".format(face))
        image = io.imread(face)

        rects = detector(image, 1)

        for (i, rect) in enumerate(rects):
            shape = predictor(image, rect)

            face_descriptor = recognitor.compute_face_descriptor(image, shape)

            features_coordinate = np.array(face_descriptor)
            face_model_list.append(features_coordinate)


def facial_feature(imagePath):
    detector, predictor ,recognitor = init_facial_model()

    image = cv2.imread(imagePath)
    image = resize(image, width = 1080)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rects = detector(image, 1)

    x = 0
    y = 0
    dist = []

    for (i, rect) in enumerate(rects):
        shape = predictor(gray, rect)
        x = rect.left()
        y = rect.top()

        face_descriptor = recognitor.compute_face_descriptor(image, shape)

        features_coordinate = np.array(face_descriptor)

        for i in face_model_list:
            np_ln = np.linalg.norm(i - features_coordinate)
            dist.append(np_ln)

# '邓丽君', '邓丽君', '邓丽君', '邓丽君', '邓丽君', 'jay', 'jay', 'jay', 'jay',
    candidate = ['邓丽君',  'jay']
    temp_dict = dict(zip(candidate, dist))

    dict_sorted = sorted(temp_dict.items(), key = lambda d:d[1])

    cv2.putText(image,
        "{}".format(dict_sorted[0][0]),
        (x - 10, y - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5, (0, 255, 0), 2)

    cv2.imshow("Output", image)
    cv2.waitKey(0)

def start():
    # if len(sys.argv) < 2:
    #     print("Usage: %s <image file>" % sys.argv[0])
    #     sys.exit(1)
    facial_model_acquisition()
    # facial_regional_marker("./imgs/test-0.jpg")
    facial_feature("./imgs/test-0.jpg")

start()
