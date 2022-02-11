import websocket
import json
import datetime
import time
import threading


def print_log(part, log_msg):
    time_now = datetime.datetime.utcnow() + datetime.timedelta(hours=-4)
    print(f"[{datetime.datetime.strftime(time_now, '%Y-%m-%d %H:%M:%S')} ({part})]: {log_msg}")


class DiscordListener:
    def __init__(self, user_token, listen_channels, sms_sender):
        self.user_token = user_token
        self.listen_channels = listen_channels
        self.ws = websocket.WebSocket()

        self.sms_sender = sms_sender

    def send_json_request(self, request):
        self.ws.send(json.dumps(request))

    def receive_json_response(self):
        response = self.ws.recv()
        if response:
            return json.loads(response)

    def send_heartbeat(self, interval):
        print_log("Discord Listener", f'Heartbeat begin - Sleeping Interval: {interval}s')
        time.sleep(interval)
        hb_json = {
            "op": 1,
            "d": None
        }
        self.send_json_request(hb_json)

    def connect(self):
        print_log("Discord Listener", "Connecting to discord gateway")
        self.ws.connect('wss://gateway.discord.gg/?v=9&encoding=json')
        event = self.receive_json_response()

        heartbeat_interval = event['d']['heartbeat_interval'] / 1000
        hb_manager = threading.Thread(target=self.send_heartbeat, args=(heartbeat_interval,))
        hb_manager.start()

        payload = {
            'op': 2,
            "d": {
                "token": self.user_token,
                "properties": {
                    "$os": "windows",
                    "$browser": "chrome",
                    "$device": 'pc'
                }
            }
        }
        self.send_json_request(payload)

    def start(self):
        self.connect()
        while True:
            event = self.receive_json_response()
            if event and event['t'] == "MESSAGE_CREATE" and event['d']['channel_id'] in self.listen_channels:
                content = event['d']['content']
                # Embed support to be added
                embeds = event['d']['embeds']

                self.sms_sender.send_message(f"Channel ID: {event['d']['channel_id']}\n"
                                             f"Content: {content}")


def create_discord_listener(setting_dict, sms_sender) -> DiscordListener:
    discord_setting = setting_dict['discord_setting']

    return DiscordListener(
        user_token=discord_setting["user_token"],
        listen_channels=discord_setting["listen_channels"],
        sms_sender=sms_sender
    )
