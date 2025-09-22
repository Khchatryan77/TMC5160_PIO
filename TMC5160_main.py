from machine import Pin, SPI, UART
from Config import Config, Motors
from tmc5160 import tmc5160
from PIO import ASM_PIO
import utime

uart = UART(0, baudrate=128000, tx=Pin(12), rx=Pin(13))

buffer = []

Board_id = 'Hand_1'

done_pin = Pin(11, Pin.OUT)

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
x_driver.IHOLD_IRUN(IHOLD= 8, IRUN=16)
x_driver.CHOPCONF(MRES = 8)

    
y_driver.GCONF()
y_driver.IHOLD_IRUN(IHOLD= 8, IRUN=16)
y_driver.CHOPCONF(MRES = 8)

x_motor_driver = ASM_PIO(x_motor)
utime.sleep_us(10)
x_motor_driver.move_motor(steps=400, dir_val=1, freq=70000)


y_motor_driver = ASM_PIO(y_motor)
utime.sleep_us(10)
y_motor_driver.move_motor(steps=400, dir_val=1, freq=70000)


while True:
    '''
    print('Start_stop_X', x_motor.Start.value())
    print('End_stop_X', x_motor.End.value())
    print('Start_stop_Y', y_motor.Start.value())
    print('End_stop_Y', y_motor.End.value())

    
    print('buffer', buffer)
    '''    
    while len(buffer) > 0:
        if buffer and buffer[0] == 'OPEN':
            integer_x = 1
            integer_y = 1
            start_stop_x = 1
            start_stop_y = 1
            motor_finished = 1
            
            uart_send('Received_Command')
            start = utime.ticks_ms()
            while x_motor.Start.value()==1 or y_motor.Start.value() == 1:
                now = utime.ticks_ms()
                if integer_x == 1:
                    
                    x_motor_driver.move_motor(steps=9600, dir_val=1, freq=250000)
                    
                    integer_x = 0
                    
                elif integer_y == 1:
                    
                    y_motor_driver.move_motor(steps=9600, dir_val=1, freq=250000)
                    
                    integer_y = 0
                    
                elif x_motor.Start.value() == 0 and start_stop_x == 1:
                    
                    x_motor_driver.stop_all()
                    print("X_endstop stopped")
                    start_stop_x = 0
                    
                elif y_motor.Start.value() == 0 and start_stop_y == 1:
                    
                    y_motor_driver.stop_all()
                    print("Y_endstop stopped")
                    start_stop_y = 0
                    
                #elif x_motor_driver.check_motors() == True and y_motor_driver.check_motors() == True and motor_finished == 1:
                    #motor_finished = 0
                    
                elif utime.ticks_diff(now, start) >= 5000 and motor_finished == 1:
                    uart_send("ERROR_IN_OPEN")
                    motor_finished = 0
                    
                utime.sleep_ms(5)
                
            x_motor_driver.stop_all()
            y_motor_driver.stop_all()
            uart_send('MOTORS_DONE')
            buffer.pop(0)
            
        
        elif buffer and buffer[0] == 'CLOSE':
            integer_x = 1
            integer_y = 1
            end_stop_x = 1
            end_stop_y = 1
            motor_finished = 1
            
            uart_send('Received_Command')
            start = utime.ticks_ms()
            while x_motor.End.value()==1 or y_motor.End.value() == 1:
                now = utime.ticks_ms()
                if integer_x == 1:
                    x_motor_driver.move_motor(steps=9600, dir_val=0, freq=250000)
                    integer_x = 0
                elif integer_y == 1:
                    y_motor_driver.move_motor(steps=9600, dir_val=0, freq=250000)
                    integer_y = 0
                elif x_motor.End.value() == 0 and end_stop_x == 1:
                    
                    x_motor_driver.stop_all()
                    print("X_endstop stopped")
                    end_stop_x = 0
                    
                elif y_motor.End.value() == 0 and end_stop_y == 1:
                    
                    y_motor_driver.stop_all()
                    print("Y_endstop stopped")
                    end_stop_y = 0
                    
                elif utime.ticks_diff(now, start) >= 5000 and motor_finished == 1:
                    uart_send("ERROR_IN_CLOSE")
                    motor_finished = 0
                    
                utime.sleep_ms(5)
                
            x_motor_driver.stop_all()
            y_motor_driver.stop_all()
            uart_send('MOTORS _DONE')
            buffer.pop(0)
        
        elif  buffer and buffer[0] == 'STATE':
            if x_motor.Start.value()==0 and y_motor.Start.value() == 0:
                uart_send('STATE_OPEN')
                
            elif x_motor.End.value()==0 and y_motor.End.value() == 0:
                uart_send('STATE_CLOSED')
                
            else:
                uart_send('STATE_ERROR')
                
            buffer.pop(0)
            
        elif  buffer and buffer[0] == '@WHO':
            print('got WHO command')
            uart_send(Board_id)
            buffer.pop(0)
            
        else:
            uart_send('ERROR_COMMAND')
            buffer.pop(0)
        
    #buffer= []
    utime.sleep(0.1)
