from pyfcm import FCMNotification
import firebase_admin
from firebase_admin import credentials, messaging

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
API_KEY = ""


def sendPush(title, msg, registration_token, dataObject=None):
    # See documentation on defining a message payload.
    message = messaging.MulticastMessage(
        notification=messaging.Notification(title=title, body=msg),
        data=dataObject,
        tokens=registration_token,
    )

    # Send a message to the device corresponding to the provided
    # registration token.
    messaging.send_multicast(message)


def sendNotification(title, msg, registration_token, dataObject=None):
    push_service = FCMNotification(api_key=API_KEY)
    push_service.notify_single_device(
        registration_id=registration_token, message_title=title, message_body=msg
    )
