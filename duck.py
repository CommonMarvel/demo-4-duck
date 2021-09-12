import json
import time

import schedule
import urllib3

token = ""

offset = 0


def pull_msg():
    global offset
    http = urllib3.PoolManager()
    resp = http.request(method="GET",
                        headers={
                            "Content-Type": "application/json",
                        },
                        url="https://api.telegram.org/bot{0}/getUpdates?offset={1}".format(token, offset))

    body = json.loads(resp.data.decode("utf-8"))
    # print(body)

    # process body for loop and update offset
    for i in range(0, len(body["result"])):
        print(body["result"][i])

        # parse sender id and process text then respond(send_msg)
        sender_id = body["result"][i]["message"]["from"]["id"]
        text = body["result"][i]["message"]["text"]

        send_msg(sender_id, text)

        if i == len(body["result"]) - 1:
            offset = body["result"][i]["update_id"] + 1


def send_msg(sender_id, text):
    http = urllib3.PoolManager()
    resp = http.request(method="POST",
                        headers={
                            "Content-Type": "application/json",
                        },
                        url="https://api.telegram.org/bot{0}/sendMessage".format(token),
                        body=json.dumps(
                            {
                                "chat_id": sender_id,
                                "text": text
                            })
                        )


if __name__ == "__main__":
    schedule.every(3).seconds.do(pull_msg)

    while True:
        schedule.run_pending()
        time.sleep(1)
