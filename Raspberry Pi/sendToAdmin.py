from firebase_admin import firestore
import FCMManager as fcm
import base64

tokens = []


def sendToAdmin(img_encoded, texta):
    global count
    db = firestore.client()
    encoded_string = ""
    encoded_string = base64.b64encode(img_encoded)
    encoded_string = encoded_string.decode("utf-8")
    docs = db.collection("Admin").stream()
    for doc in docs:
        tokens.clear()
        id = doc.id
        users_ref = db.collection("Users").document(id)
        users_ref.update({"haveNotification": True})
        img_ref = db.collection("CurrentImage").document("current_image")
        img_ref.update({"value": str(encoded_string)})
        get_token = users_ref.get({"token"})
        token = "{}".format(get_token.to_dict()["token"])
        tokens.append(token)
        fcm.sendPush("Parking Lot", texta, tokens)
    print("Đã gửi thông báo đến Admin")
