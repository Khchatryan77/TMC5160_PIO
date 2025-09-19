from machine import Pin
import rp2
from Config import Config
    
    
class ASM_PIO():
    def __init__(self, Config):
        self.Motors = Config
        self.state_machines = {}  # store motors by ID
    
    @rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
    def stepper():

        pull()            # Get number of steps from CPU
        mov(x, osr)       # Move to X register
        label("loop")
        jmp(x_dec, "pulse")
        jmp("end")
        
        label("pulse")
        set(pins, 1) [31]  # Pulse HIGH
        set(pins, 0) [31]  # Pulse LOW
        jmp("loop")
        
        label("end")
        nop()              # End program    


    def move_motor(self, steps, dir_val, freq = 400_000):  # move with STEP/DIR

        Step_Pin = self.Motors.Step
        Dir_Pin = self.Motors.Dir
        Sm_id = self.Motors.Sm_id

        Dir_Pin.value(dir_val)

        sm = rp2.StateMachine(Sm_id, ASM_PIO.stepper, freq=freq, set_base=Step_Pin)
        self.state_machines[Sm_id] = sm
        sm.active(1)
        sm.put(steps)

    def stop_all(self):
        for sm_id in self.state_machines:
            self.state_machines[sm_id].active(0)

