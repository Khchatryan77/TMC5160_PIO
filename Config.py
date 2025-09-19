from machine import Pin

Motors = {
    'X': {
        'Step_Pin': 8,
        'Dir_Pin': 7,
        'En': None,
        'Start_switch': 26,
        'End_switch': 27,
        'Sm_id': 0,
        'CS_Pin': 6,
        'Length_mm': 10000,
        'MIN_SPEED': 100,
        'MAX_SPEED': 2000,
        'ACCEL': 500,
        'DECCEL': 500,
    },

    'Y': {
        'Step_Pin': 4,
        'Dir_Pin': 5,
        'En': None,
        'Start_switch': 15,
        'End_switch': 14,
        'Sm_id': 1,
        'CS_Pin': 1,
        'Length_mm': 10000,
        'MIN_SPEED': 100,
        'MAX_SPEED': 2000,
        'ACCEL': 500,
        'DECCEL': 500,
    },
}

class Config:
    def __init__(self, data: dict):
        # Setup pins here
        self.Step = Pin(data['Step_Pin'], Pin.OUT)
        self.Dir = Pin(data['Dir_Pin'], Pin.OUT)
        #self.En = Pin(data['En_Pin'], Pin.OUT)
        self.CS = Pin(data['CS_Pin'], Pin.OUT)
        self.Start = Pin(data['Start_switch'], Pin.IN, Pin.PULL_UP)
        self.End = Pin(data['End_switch'], Pin.IN, Pin.PULL_UP)

        # Motion parameters
        self.Length_mm = data['Length_mm']
        self.MIN_SPEED = data['MIN_SPEED']
        self.MAX_SPEED = data['MAX_SPEED']
        self.ACCEL = data['ACCEL']
        self.DECCEL = data['DECCEL']
        self.Sm_id = data['Sm_id']