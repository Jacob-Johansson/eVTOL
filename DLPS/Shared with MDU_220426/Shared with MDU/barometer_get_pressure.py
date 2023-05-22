import board
import adafruit_bmp3xx

# I2C setup
i2c = board.I2C()  # uses board.SCL and board.SDA
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)

bmp.pressure_oversampling = 8

def get_pressure():
    return bmp.pressure
