from picamera import PiCamera
import requests
import numpy as np
import cv2
from firebase_admin import firestore
from sendToAdmin import sendToAdmin
import servo
import checkIn
import json

camera = PiCamera()
camera.resolution = (640, 480)
content_type = "image/jpeg"
headers = {"content-type": content_type}
db = firestore.client()
licenseNumber = ""
tryCount = 0


def saveIn(doc_ref):
    print("Xe dang ngoai bai, cho xe di vao")
    get_id = doc_ref.get({"id"})
    id = "{}".format(get_id.to_dict()["id"])
    users_ref = db.collection("Users").document(id)
    get_name = users_ref.get({"name"})
    name = "{}".format(get_name.to_dict()["name"])
    get_admin = users_ref.get({"admin"})
    admin = "{}".format(get_admin.to_dict()["admin"])
    admin = admin == "True"
    checkin = True  # vao
    data = {
        "id": id,
        "time": firestore.SERVER_TIMESTAMP,
        "name": name,
        "admin": admin,
        "checkin": checkin,
    }
    db.collection("TimeInOut").add(data)
    print("saved!")


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
    if (
        len(response.text) > 1
    ):  # neu co hoi dap tu server thi thuc hien, k thi bo qua va gui anh tiep
        print(response.text)
        typeVehicle, license1 = response.text.split("-")
        if not checkIn.TrueResult(typeVehicle, license1):
            print("khong du ky tu")
            tryCount = 0
            continue
        elif licenseNumber != license1:  # neu nhan kq khac lan gui truoc
            print(license1)
            doc_ref = db.collection("LicensePlateNumber").document(license1)
            doc = doc_ref.get()
            tryCount += 1
            if doc.exists:
                print("exist")
                if not checkIn.ParkingCheck(doc_ref, db):
                    saveIn(doc_ref)
                    servo.dongmocong()
                    tryCount = 0
                else:
                    print("Luu roi di ra khoi lan")
                    tryCount = 0
            elif tryCount > 2:  # else:#nhan dien sai, de admin snhan dien
                print("Loi nhan dien")
                sendToAdmin(img_encoded, "Kiem tra nhan dien")
                license1 = requests.get(
                    "http://detectparking.ddns.net/selfPredict/"
                ).text
                while license1 == "None":
                    license1 = requests.get(
                        "http://detectparking.ddns.net/selfPredict/"
                    ).text
                    continue
                dict = license1
                res = json.loads(dict)
                license1 = str(res["command"])
                print(license1)
                doc_ref = db.collection("LicensePlateNumber").document(license1)
                doc = doc_ref.get()
                if doc.exists:  # true
                    if not checkIn.ParkingCheck(doc_ref, db):
                        saveIn(doc_ref)
                        servo.dongmocong()
                        tryCount = 0
                    else:
                        print("Luu roi di ra khoi lan")
                        tryCount = 0
                else:  # chua dang ky
                    print("Chua dang ky tai khoan")
                    tryCount = 0
            licenseNumber = license1
        else:
            print("Trung lap bien so")
            tryCount = 0
    else:
        print("khong co xe")
        tryCount = 0
        continue
