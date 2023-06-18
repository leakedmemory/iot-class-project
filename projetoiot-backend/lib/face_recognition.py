import face_recognition as fr
import cv2
from PIL import Image
import base64
import io
import numpy as np
from lib.database import get_users_container


def find_target_face(target_img, users_to_compare):
    user_info = dict()

    face_location = fr.face_locations(target_img)
    face_encoding = fr.face_encodings(target_img)

    if not face_location or not face_encoding:
        user_info["user_name"] = "Unknown"
        user_info["allowed"] = False
        return user_info

    for person in users_to_compare:
        encoded_face = person[0]

        is_target_face = fr.compare_faces(encoded_face, face_encoding, tolerance=0.55)

        if face_location:
            face_number = 0
            for location in face_location:
                if is_target_face[face_number]:
                    user_info["user_name"] = person[1]
                    user_info["allowed"] = True
                    return user_info
                face_number += 1

    user_info["user_name"] = "Unknown"
    user_info["allowed"] = False
    return user_info


def image_to_ndarray(image_base64):
    im_bytes = base64.b64decode(image_base64)
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
    img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
    known_encoding = fr.face_encodings(img)

    if not known_encoding:
        return None
    return list(known_encoding[0])


def get_users_to_compare():
    users_container = get_users_container()

    def has_image_ndarray(user):
        return user["image_ndarray"]

    def map_user(user):
        return [np.array(user["image_ndarray"]), user["user_name"], user["id"]]

    filtered_users = list(filter(
        has_image_ndarray,
        users_container.query_items(
            "SELECT u.id, u.image_ndarray, u.user_name FROM users u",
            enable_cross_partition_query=True,
        )
    ))

    return list(map(map_user, filtered_users))


def check_user_permission(image_base64):
    users_to_compare = get_users_to_compare()

    im_bytes = base64.b64decode(image_base64)
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
    img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
    return find_target_face(img, users_to_compare)
