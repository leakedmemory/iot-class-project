import azure.functions as func
import uuid
import logging
from lib.database import get_users_container
from lib.json import to_json
from lib.storage import upload_blob
import re
from lib.face_recognition import image_to_ndarray


def create_user_use_case(req_data):
    users_container = get_users_container()
    data_to_save = dict()

    data_to_save["id"] = str(uuid.uuid4())
    data_to_save["image_ndarray"] = image_to_ndarray(req_data["image"])
    data_to_save["user_name"] = req_data["user_name"]

    user = users_container.create_item(data_to_save)
    return user


def main(req: func.HttpRequest) -> func.HttpResponse:
    body = req.get_json()
    result = create_user_use_case(body)
    response = to_json(result)

    return func.HttpResponse(response, status_code=201)
