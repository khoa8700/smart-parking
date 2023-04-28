from picamera import PiCamera

import requests
import numpy as np
import cv2
from FCMManager import sendPush
from firebase_admin import firestore
from sendToAdmin import sendToAdmin
import servo
import checkIn
import json

db = firestore.client()

camera = PiCamera()
camera.resolution = (640, 480)
content_type = "image/jpeg"
headers = {"content-type": content_type}
licenseNumber = "a"
tokens = []
tryCount = 0


def saveOut(doc_ref):
    tokens.clear()
    print("Xe dang trong bai, cho xe di ra")
    get_id = doc_ref.get({"id"})
    id = "{}".format(get_id.to_dict()["id"])
    print("id:", id)
    users_ref = db.collection("Users").document(id)
    # admin=admin=='True'
    get_token = users_ref.get({"token"})
    token = "{}".format(get_token.to_dict()["token"])
    users_ref.update({"haveNotification": True})
    checkin = False  # ra
    tokens.append(token)
    sendPush("xac nhan lay xe", "xac nhan lay xe?", tokens)
    print("Dang doi xac nhan lay xe...")
    res = requests.get("http://detectparking.ddns.net/auth/").text
    while res == "None":
        res = requests.get("http://detectparking.ddns.net/auth/").text
        continue
    dict = res
    res = json.loads(dict)
    license1 = str(res["command"])
    # 	print(type(license1))
    print(license1)
    if license1 == "YES":
        get_name = users_ref.get({"name"})
        name = "{}".format(get_name.to_dict()["name"])
        get_admin = users_ref.get({"admin"})
        admin = "{}".format(get_admin.to_dict()["admin"])
        admin = admin == "True"
        data = {
            "id": id,
            "time": firestore.SERVER_TIMESTAMP,
            "name": name,
            "admin": admin,
            "checkin": checkin,
        }
        db.collection("TimeInOut").add(data)
        print("saved!")
        servo.dongmocong()
    else:
        print("an trom")


while True:
    output = np.empty((480, 640, 3), dtype=np.uint8)
    camera.capture(output, "rgb")
    output = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
    _, img_encoded = cv2.imencode(".jpg", output)
    response = requests.post(
        "http://detectparking.ddns.net/predict/",
        headers=headers,
        data=img_encoded.tobytes(),
    )
    if len(response.text) > 1:
        print(response.text)
        typeVehicle, license1 = response.text.split("-")
        if not checkIn.TrueResult(typeVehicle, license1):
            print("khong du ky tu")
            tryCount = 0
            continue
        elif licenseNumber != license1:
            print(license1)
            doc_ref = db.collection("LicensePlateNumber").document(license1)
            doc = doc_ref.get()
            tryCount += 1
            # print(tryCount)
            if doc.exists:
                if checkIn.ParkingCheck(doc_ref, db):  # False
                    saveOut(doc_ref)
                    tryCount = 0
                else:
                    print("Xe dang o ngoai roi")
                    tryCount = 0

            elif tryCount > 2:
                print("Loi nhan dien")
                sendToAdmin(img_encoded, "Kiem tra xe ra")
                license1 = requests.get(
                    "http://detectparking.ddns.net/selfPredict/"
                ).text
                while license1 == "None":
                    license1 = requests.get(
                        "http://detectparking.ddns.net/selfPredict/"
                    ).text
                    continue
                print(license1)
                dict = license1
                res = json.loads(dict)
                license1 = str(res["command"])
                print(license1)

                doc_ref = db.collection("LicensePlateNumber").document(license1)
                doc = doc_ref.get()
                if doc.exists:  # true
                    if checkIn.ParkingCheck(doc_ref, db):
                        saveOut(doc_ref)
                        tryCount = 0
                    else:
                        print("Luu roi di ra khoi lan")
                        tryCount = 0
                else:
                    print("Tai khoan da bi xoa")
                    tryCount = 0
            licenseNumber = license1
        else:
            print("Trung lap bien so")
            tryCount = 0
    else:
        print("khong co xe")
        tryCount = 0
        continue
