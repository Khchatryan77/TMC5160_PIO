from machine import Pin, SPI, UART
from Config import Config, Motors
from tmc5160 import tmc5160
from PIO import ASM_PIO
import utime

uart = UART(0, baudrate=128000, tx=Pin(12), rx=Pin(13))

buffer = []

Board_id = 'Hand_1'

def uart_handler(uart):
    if uart.any():  
        data = uart.read().decode().strip()  
        buffer.append(data)
        print("Received:", data)
        return data
    
def uart_send(data):
    uart.write(data + '\r\n')

uart.irq(trigger = UART.IRQ_RXIDLE, handler = uart_handler)

# SPI pins
SPI_SCK = Pin(2, Pin.OUT)
SPI_MOSI = Pin(3, Pin.OUT)
SPI_MISO = Pin(0, Pin.IN)

spi = SPI(0, baudrate=1000000, polarity=0, phase=0,
          sck=SPI_SCK, mosi=SPI_MOSI, miso=SPI_MISO)

x_motor = Config(Motors['X'])
y_motor = Config(Motors['Y'])

x_driver = tmc5160(spi, Motors['X']['CS_Pin'])
y_driver = tmc5160(spi, Motors['Y']['CS_Pin'])

    
x_driver.GCONF()
x_driver.IHOLD_IRUN(IHOLD= 4, IRUN=12)
x_driver.CHOPCONF(MRES = 4)

    
y_driver.GCONF()
y_driver.IHOLD_IRUN(IHOLD= 4, IRUN=12)
y_driver.CHOPCONF(MRES = 4)

x_motor_driver = ASM_PIO(x_motor)
utime.sleep_us(10)
x_motor_driver.move_motor(steps=800, dir_val=1, freq=30000)

y_motor_driver = ASM_PIO(y_motor)
utime.sleep_us(10)
y_motor_driver.move_motor(steps=800, dir_val=1, freq=30000)


while True:
    print('Start_stop_X', x_motor.Start.value())
    print('End_stop_X', x_motor.End.value())
    print('Start_stop_Y', y_motor.Start.value())
    print('End_stop_Y', y_motor.End.value())
    
    print('buffer', buffer)
    while len(buffer) > 0:
        if buffer and buffer[0] == 'move_motors':
            integer = 1
            while x_motor.Start.value() == 1:
                if integer == 1:
                    
                    x_motor_driver.move_motor(steps=4800, dir_val=1, freq=50000)
                    y_motor_driver.move_motor(steps=4800, dir_val=1, freq=50000)
                    
                    integer = 0
                    
            x_motor_driver.stop_all()
            y_motor_driver.stop_all()
            buffer.pop(0)
            
        elif  buffer and buffer[0] == '@WHO':
            print('got WHO command')
            uart_send(Board_id)
            buffer.pop(0)
            
        else:
            uart_send('ERROR')
            buffer.pop(0)
        
    #buffer= []
    utime.sleep(0.1)
