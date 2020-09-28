import json

import requests

serverToken = "AAAAETYLnBQ:APA91bHr0YFzCDqVvbp5BSXZBNFXAGV_GIZsnRBhgrwpHDBEgZariRCMkCBejn8ZKZ-DqrFHsIjUh75nzl0_TGEPt0f2Gs488Vm8AoW9TfyQzT67RmYYiWnXc36Yb6StbGrOTbWixWMX"


def send_notification(device_id, data, title, message_body):
    print("device id",device_id)
    headers = {
        "Content-Type": "application/json",
        "Authorization": "key=" + serverToken
    }

    body = {
        'notification': {'title': title,
                         'body': message_body
                         },
        'to': device_id,
        'priority': 'high',
        'data': data,
    }
    response = requests.post("https://fcm.googleapis.com/fcm/send", headers=headers, data=json.dumps(body))
    print(response.status_code)

    print(response.json())
    return response
