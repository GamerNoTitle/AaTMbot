class missionNode:
    def __init__(self, data: dict):
        self.type = data.get('missionType', data.get('type', None))
        self.modifier = data.get('modifier', None)
        self.modifierDescription = data.get('modifierDescription', None)
        self.node = data['node']
