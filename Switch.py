class Switch:
    enabled = False  # set enabled default to false

    def __init__(self, group: int, num: int, name: str, code_on: str, code_off: str, is_multi_switch=False):
        self.group = group
        self.num = num
        self.name = name
        self.code_on = code_on
        self.code_off = code_off
        self.is_multi_switch = is_multi_switch

    def __repr__(self):
        return f'{self.num}: {self.name}: {self.enabled}: {self.code_on}: {self.code_off}'

    def __str__(self):
        return f'{self.num}: {self.name}: {self.enabled}'

    def toSimpleJSON(self):
        class simpleSwitch:  # inner class to make json.dumps work seamless
            def __init__(self, num, enabled):
                self.num = num
                self.enabled = enabled
        return simpleSwitch(self.num, self.enabled)
