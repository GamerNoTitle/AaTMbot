class missionNode:
    def __init__(self, data: dict):
        self.type = data['missionType']
        self.modifier = data.get('modifier', None)
        self.modifierDescription = data.get('modifierDescription', None)
        self.node = data['node']
        