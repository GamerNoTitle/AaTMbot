class message:
    def __init__(self, message: dict):
        self.type = message['message_type']
        if self.type == 'private':
            self.message = message['raw_message']
            self.message_id = message['message_id']
            self.group_id = -1
            self.user_id = message['user_id']
        else:
            self.message = message['raw_message']
            self.message_id = message['message_id']
            self.group_id = message['group_id']
            self.user_id = message['user_id']