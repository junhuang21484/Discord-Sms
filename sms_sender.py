from twilio.rest import Client
import datetime


def print_log(part, log_msg):
    time_now = datetime.datetime.utcnow() + datetime.timedelta(hours=-4)
    print(f"[{datetime.datetime.strftime(time_now, '%Y-%m-%d %H:%M:%S')} ({part})]: {log_msg}")


class SmsSender:
    def __init__(self, account_sid, auth_token, twilio_number, receiving_number):
        self.client = Client(account_sid, auth_token)

        self.twilio_number = twilio_number
        self.receiving_number = receiving_number

    def send_message(self, message: str):
        message = self.client.messages.create(
            body="\n" + message,
            from_=self.twilio_number,
            to=self.receiving_number
        )

        print_log("SMS SENDER", message.sid)


def create_sender(setting_dict) -> SmsSender:
    sender_setting = setting_dict['sms_setting']

    return SmsSender(
        account_sid=sender_setting['account_id'],
        auth_token=sender_setting['auth_token'],
        twilio_number=sender_setting['twilio_number'],
        receiving_number=sender_setting['receiving_number']
    )