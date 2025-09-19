from machine import Pin, SPI
import utime

# SPI pins
SPI_SCK = Pin(2, Pin.OUT)
SPI_MOSI = Pin(3, Pin.OUT)
SPI_MISO = Pin(0, Pin.IN)

spi = SPI(0, baudrate=1000000, polarity=0, phase=0,
          sck=SPI_SCK, mosi=SPI_MOSI, miso=SPI_MISO)


class tmc5160:
    
    W = 0x80
    R = 0x00

    REG_GCONF      = 0x00
    REG_GSTAT      = 0x01
    REG_IHOLD_IRUN = 0x10
    REG_TPOWERDOWN = 0x11
    REG_TSTEP      = 0x12
    REG_TPWMTHRS   = 0x13
    REG_CHOPCONF   = 0x6C
    REG_COOLCONF   = 0x6D
    REG_PWMCONF    = 0x70
    
    def __init__(self, spi, cs_pin):
        self.spi = spi
        self.SPI_CS = Pin(cs_pin, Pin.OUT)
        self.SPI_CS.value(1)
        
    
    def tmc_write(self, register, value):
        self.SPI_CS.value(0)  
        first_byte = self.W | register
        packet = bytearray([
            first_byte,
            (value >> 24) & 0xFF,
            (value >> 16) & 0xFF,
            (value >> 8) & 0xFF,
            (value & 0xFF)
        ])
        val = int.from_bytes(packet, "big")
        print(hex(val))
        self.spi.write(packet)
        self.SPI_CS.value(1)  

    def tmc_read(self, register):
          
        self.SPI_CS.value(0)
        self.spi.write(bytearray([self.R | register, 0, 0, 0, 0]))
        self.SPI_CS.value(1)

        self.SPI_CS.value(0)
        response = bytearray(5)
        self.spi.readinto(response)
        self.SPI_CS.value(1)

        value = int.from_bytes(response[1:], "big")
        return hex(value)
    

    def GCONF(self):
        packet = [0x00, 0x00, 0x00, 0x14]
        value = (packet[0]<<24) | (packet[1]<<16) | (packet[2]<<8) | packet[3]
        self.tmc_write(self.REG_GCONF, value)
        return self.tmc_read(self.REG_GCONF)
    
    def CHOPCONF(self, MRES):
        if MRES == 1:
            packet = [0x18, 0x01, 0x40, 0xC3]
            
        elif MRES == 2:
            packet = [0x17, 0x01, 0x40, 0xC3]
        
        elif MRES == 4:
            packet = [0x16, 0x01, 0x40, 0xC3]
        
        elif MRES == 8:
            packet = [0x15, 0x01, 0x40, 0xC3]
            
        elif MRES == 16:
            packet = [0x14, 0x01, 0x40, 0xC3]
            
        elif MRES == 32:
            packet = [0x13, 0x01, 0x40, 0xC3]
            
        elif MRES == 64:
            packet = [0x12, 0x01, 0x40, 0xC3]
            
        elif MRES == 128:
            packet = [0x11, 0x01, 0x40, 0xC3]
            
        elif MRES == 256:
            packet = [0x10, 0x01, 0x40, 0xC3]
            
        #packet = [0x18, 0x01, 0x40, 0xC3]			 #default [0x10, 0x41, 0x01, 0x53]  
        value = (packet[0]<<24) | (packet[1]<<16) | (packet[2]<<8) | packet[3]
        self.tmc_write(self.REG_CHOPCONF, value)
        return self.tmc_read(self.REG_CHOPCONF)
    
    
    def IHOLD_IRUN(self, IHOLD, IRUN):
        
        if IHOLD == 0:
            IHOLD_val = 0x00
        elif IHOLD == 1:
            IHOLD_val = 0x01
        elif IHOLD == 2:
            IHOLD_val =0x02
        elif IHOLD == 4:
            IHOLD_val =0x04
        elif IHOLD == 8:
            IHOLD_val =0x08
        elif IHOLD == 12:
            IHOLD_val =0x0C
        elif IHOLD == 16:
            IHOLD_val =0x10
        elif IHOLD == 20:
            IHOLD_val =0x14
        elif IHOLD == 24:
            IHOLD_val =0x18
        elif IHOLD == 28:
            IHOLD_val =0x1C
        elif IHOLD == 31:
            IHOLD_val =0x1F
        else:
            raise ValueError("Invalid IHOLD value")
            
        if IRUN == 0:
            IRUN_val =0x00
        elif IRUN == 1:
            IRUN_val =0x01
        elif IRUN == 2:
            IRUN_val =0x02
        elif IRUN == 4:
            IRUN_val =0x04
        elif IRUN == 8:
            IRUN_val =0x08
        elif IRUN == 12:
            IRUN_val =0x0C
        elif IRUN == 16:
            IRUN_val =0x10
        elif IRUN == 20:
            IRUN_val =0x14
        elif IRUN == 24:
            IRUN_val =0x18
        elif IRUN == 28:
            IRUN_val =0x1C
        elif IRUN == 31:
            IRUN_val =0x1F
        else:
            raise ValueError("Invalid IRUN value")
            
        packet = [0x00, 0x06, IRUN_val, IHOLD_val]
        
        #packet = [0x00, 0x00, 0x1F, 0x05] #[0x00, 0x16, 0x08, 0x08]
        value = (packet[0]<<24) | (packet[1]<<16) | (packet[2]<<8) | packet[3]
        self.tmc_write(self.REG_IHOLD_IRUN, value)
        return self.tmc_read(self.REG_IHOLD_IRUN)
        
        

