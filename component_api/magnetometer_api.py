import math

from machine import Pin, I2C
import time

class Magnetometer:
    """
    API for HMC5883L magnetometer sensor
    """
    # Magnetometer I2C address
    HMC5883L_ADDR = 0x1E  # Default I2C address for the HMC5883L
    
    # Registers
    CONFIG_REG_A = 0x00
    CONFIG_REG_B = 0x01
    MODE_REG = 0x02
    DATA_REG_BEGIN = 0x03
    
    def __init__(self, i2c_id=0, scl_pin=5, sda_pin=4):
        """
        Initialize the magnetometer.
        
        Args:
            i2c_id: I2C bus id
            scl_pin: SCL pin number
            sda_pin: SDA pin number
        """
        # Initialize I2C
        self.i2c = I2C(i2c_id, scl=Pin(scl_pin), sda=Pin(sda_pin))
        
        # Initialize magnetometer
        self._init_hmc5883l()
    
    def _init_hmc5883l(self):
        """Configure the magnetometer for continuous measurement"""
        # Configuration register A: 8-average, 15 Hz, normal mode
        self.i2c.writeto(self.HMC5883L_ADDR, bytearray([self.CONFIG_REG_A, 0x70]))
        
        # Configuration register B: Gain = 5
        self.i2c.writeto(self.HMC5883L_ADDR, bytearray([self.CONFIG_REG_B, 0xA0]))
        
        # Mode register: Continuous measurement mode
        self.i2c.writeto(self.HMC5883L_ADDR, bytearray([self.MODE_REG, 0x00]))
    
    def read_raw_data(self):
        """
        Read the raw X, Y, Z magnetometer values.
        
        Returns:
            Tuple of (x, y, z) raw values
        """
        # Read 6 bytes of data from address 0x03 (X, Y, Z registers)
        data = self.i2c.readfrom_mem(self.HMC5883L_ADDR, self.DATA_REG_BEGIN, 6)
        
        # Convert the data
        x = (data[0] << 8) | data[1]
        y = (data[2] << 8) | data[3]
        z = (data[4] << 8) | data[5]
        
        # Handle negative values (two's complement)
        if x >= 0x8000:
            x -= 0x10000
        if y >= 0x8000:
            y -= 0x10000
        if z >= 0x8000:
            z -= 0x10000
            
        return x, y, z
    
    def read_heading(self):
        """
        Calculate heading in degrees (0-359)
        
        Returns:
            Heading angle in degrees from North (0-359)
        """
        x, y, z = self.read_raw_data()
        
        # Calculate heading
        if y > 0:
            heading = 90 - (180/3.14159) * (math.atan(x/y))
        elif y < 0:
            heading = 270 - (180/3.14159) * (math.atan(x/y))
        elif x < 0:
            heading = 180.0
        else:
            heading = 0.0
            
        # Ensure heading is between 0-359 degrees
        heading = heading % 360
        
        return heading
    
    def get_calibrated_values(self, offset_x=0, offset_y=0, offset_z=0, scale_x=1, scale_y=1, scale_z=1):
        """
        Get calibrated magnetometer values
        
        Args:
            offset_x, offset_y, offset_z: Calibration offsets
            scale_x, scale_y, scale_z: Calibration scaling factors
            
        Returns:
            Tuple of calibrated (x, y, z) values
        """
        x, y, z = self.read_raw_data()
        
        # Apply calibration
        cal_x = (x - offset_x) * scale_x
        cal_y = (y - offset_y) * scale_y
        cal_z = (z - offset_z) * scale_z
        
        return cal_x, cal_y, cal_z
