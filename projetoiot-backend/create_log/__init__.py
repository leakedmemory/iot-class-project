import azure.functions as func
import uuid
import logging
from lib.database import get_logs_container
from lib.json import to_json
from lib.storage import upload_blob
from lib.face_recognition import check_user_permission
import re
from datetime import datetime


def create_log_use_case(req_data):
    logs_container = get_logs_container()
    data_to_save = dict()
    data_to_save["id"] = str(uuid.uuid4())

    filename = upload_blob(
        data=req_data["image"],
        filename=data_to_save["id"],
        container="access"
    )
    data_to_save["image"] = filename

    user_info = check_user_permission(req_data["image"])

    data_to_save["user_name"] = user_info["user_name"]
    data_to_save["allowed"] = user_info["allowed"]
    data_to_save["created_at"] = str(datetime.now())

    user = logs_container.create_item(data_to_save)

    return user


def main(req: func.HttpRequest) -> func.HttpResponse:
    body = req.get_json()
    result = create_log_use_case(body)
    response = to_json(result)

    return func.HttpResponse(response, status_code=201)
