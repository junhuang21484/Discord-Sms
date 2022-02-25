import websocket
import json
import datetime
import time
import threading


def print_log(part, log_msg):
    time_now = datetime.datetime.utcnow() + datetime.timedelta(hours=-4)
    print(f"[{datetime.datetime.strftime(time_now, '%Y-%m-%d %H:%M:%S')} ({part})]: {log_msg}")


def parse_embeds(embed_json):
    print(embed_json)
    if embed_json:
        fields = embed_json['fields']
        embed_content = ""
        for field in fields:
            embed_content += f"{field['name']}\n{field['value']}\n"

        return embed_content

    return


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
        try:
            while True:
                print_log("Discord Listener", f'Heartbeat begin - Sleeping Interval: {interval}s')
                time.sleep(interval)
                hb_json = {
                    "op": 1,
                    "d": None
                }
                self.send_json_request(hb_json)
        except:
            print_log("CONNECTION", "Heartbeat failed to sent")

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
            try:
                event = self.receive_json_response()
                if event and event['t'] == "MESSAGE_CREATE" and event['d']['channel_id'] in self.listen_channels:
                    content = event['d']['content']
                    # Embed support to be added
                    embed_content = "" if not event['d']['embeds'] else parse_embeds(event['d']['embeds'][0])

                    if content and embed_content:
                        self.sms_sender.send_message(f"Channel ID: {event['d']['channel_id']}\n\n"
                                                     f"Text Content\n{content}\n\n"
                                                     f"Embed Content\n{embed_content}")
                    elif content:
                        self.sms_sender.send_message(f"Channel ID: {event['d']['channel_id']}\n\n"
                                                     f"Text Content\n{content}")
                    elif embed_content:
                        self.sms_sender.send_message(f"Channel ID: {event['d']['channel_id']}\n\n"
                                                     f"Embed Content\n{embed_content}")
            except websocket.WebSocketConnectionClosedException:
                print_log("CONNECTION", "Connection lost...")
                self.ws.close()

                print_log("CONNECTION", "Trying to reconnect...")
                self.connect()
                print_log("CONNECTION", f"Connection status - {self.ws.connected}")


def create_discord_listener(setting_dict, sms_sender) -> DiscordListener:
    discord_setting = setting_dict['discord_setting']

    return DiscordListener(
        user_token=discord_setting["user_token"],
        listen_channels=discord_setting["listen_channels"],
        sms_sender=sms_sender
    )
