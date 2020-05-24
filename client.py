from telethon import TelegramClient

api_id = 125011
api_hash = 'b3056065f5678acbdb69970c4c15bc84'


def get_password():
    print('getting password')
    return '+380507691229'


def get_code():
    return input()


test_chat = 248067313
release_chat = 1136733507


class Client:
    def __init__(self, phone, code_callback):
        super(Client, self).__init__()
        self.client = TelegramClient('session_name', api_id, api_hash)
        self.client.start(phone=phone, password=get_password, code_callback=code_callback)
        self.entity = self.client.loop.run_until_complete(self.client.get_entity(release_chat))

    def send_message(self, text):
        self.client.loop.run_until_complete(self.client.send_message(self.entity, text))
