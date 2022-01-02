class Switch:

    enabled = False  # set enabled default to false

    def __init__(self, num, name, code_on, code_off):
        self.num = num
        self.name = name
        self.code_on = code_on
        self.code_off = code_off

    def __repr__(self):
        return f'{self.num}: {self.name}: {self.enabled}: {self.code_on}: {self.code_off}'

    def __str__(self):
        return f'{self.num}: {self.name}: {self.enabled}'
