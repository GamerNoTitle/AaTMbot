class message:
    def __init__(self, message: dict):
        self.type = message['message_type']
        if self.type == 'private':
            self.message: str = message['raw_message']
            self.message_id: str = message['message_id']
            self.group_id: str = -1
            self.user_id: str = message['user_id']
        else:
            self.message: str = message['raw_message']
            self.message_id: str = message['message_id']
            self.group_id: str = message['group_id']
            self.user_id: str = message['user_id']