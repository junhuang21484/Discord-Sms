from sms_sender import create_sender
from discord_listener import create_discord_listener
import json
import datetime

VERSION = "V0.0.1"


def print_log(part, log_msg):
    time_now = datetime.datetime.utcnow() + datetime.timedelta(hours=-4)
    print(f"[{datetime.datetime.strftime(time_now, '%Y-%m-%d %H:%M:%S')} ({part})]: {log_msg}")


if __name__ == '__main__':
    print_log("STARTING", f"Welcome to Discord SMS! ({VERSION})")
    setting = json.load(open("setting.json", "r", encoding="UTF-8"))

    sms_sender = create_sender(setting)
    print_log("STARTING", f"SMS sender created successfully")

    discord_listener = create_discord_listener(setting, sms_sender)
    print_log("STARTING", f"Discord listener created successfully")

    discord_listener.start()

