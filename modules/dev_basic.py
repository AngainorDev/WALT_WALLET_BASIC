"""
Simple dev helpers

# Only used in micropython context
"""

from machine import Pin, SPI, PWM
import st7789


TFT = None


def dev_message():
    """Init LCD and set background green to make dev mode obvious"""
    global TFT
    TFT = st7789.ST7789(SPI(2, baudrate=30000000, polarity=1, phase=1, sck=Pin(18), mosi=Pin(19)), 135, 240,
                             reset=Pin(23, Pin.OUT), cs=Pin(5, Pin.OUT), dc=Pin(16, Pin.OUT),
                             rotation=1)
    TFT.init()
    backlight = PWM(Pin(4, Pin.OUT))
    # workaround soft reset
    backlight.deinit()
    backlight.init(freq=5000, duty=750)
    TFT.fill(0x07E0)