class invasionMission:
    def __init__(self, data: dict):
        self.id = data['id']
        self.node = data['node']
        self.attacker = data['attackingFaction']
        self.defender = data['defendingFaction']
        self.attackReward = data['attackerReward']['asString']
        self.defendReward = data['defenderReward']['asString']
        self.requiredRuns = data['requiredRuns']