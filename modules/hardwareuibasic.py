# Hardware interface layer.
# Close to the hardware, only basic primitives.

# Copyright (C) 2020-2021 Angainor
#
# Only used in micropython context


import sys
import gc
import os
import time

from machine import Pin, SPI
import st7789


class HardwareUI(object):

    def __init__(self, orientation=3):
        self.emulated = False
        self.color_bytes = 2  # 2 for hardware rgb 565, 3 for simulated RGB
        self.width = 240
        self.height = 135
        self.orientation = orientation
        self.on_event = None
        """
        self.tft = st7789.ST7789(SoftSPI(baudrate=40000000, polarity=1, phase=1, sck=Pin(18), mosi=Pin(19), miso=Pin(14)), 
                                 135, 240,
                                 reset=Pin(23, Pin.OUT), cs=Pin(5, Pin.OUT), dc=Pin(16, Pin.OUT),
                                 rotation=orientation)       
        """                         
        self.tft = st7789.ST7789(SPI(2, baudrate=30000000, polarity=1, phase=1, sck=Pin(18), mosi=Pin(19), miso=Pin(14)), 
                                 135, 240, reset=Pin(23, Pin.OUT), cs=Pin(5, Pin.OUT), dc=Pin(16, Pin.OUT),
                                 rotation=orientation)                                  
        # backlight is handled by enginebasic
        self.tft.init()
        self.rect = self.tft.rect
        self.fill_rect = self.tft.fill_rect
        self.line = self.tft.line
        self.hline = self.tft.hline
        self.vline = self.tft.vline

        self.btn = dict()
        # TODO: from config
        if self.orientation == 1:
            self.btn["UP"] = Pin(35, Pin.IN, Pin.PULL_UP)
            self.btn["DOWN"] = Pin(0, Pin.IN, Pin.PULL_UP)
        else:
            self.btn["UP"] = Pin(0, Pin.IN, Pin.PULL_UP)
            self.btn["DOWN"] = Pin(35, Pin.IN, Pin.PULL_UP)
        self.btn["UP"].irq(trigger=Pin.IRQ_FALLING, handler=self.btn_handler)
        self.btn["DOWN"].irq(trigger=Pin.IRQ_FALLING, handler=self.btn_handler)

    def btn_handler(self, pin):
        # debounce see https://wdi.centralesupelec.fr/boulanger/MicroPython/ESP32BE3
        # TODO: disable irq
        time.sleep_ms(20)
        if pin.value():
            # print("bounce")
            return
        if pin == self.btn["UP"]:
            # print("LOG: HWBTN UP")
            self.do_event("UP")
        elif pin == self.btn["DOWN"]:
            # print("LOG: HWBTN DOWN")
            self.do_event("DOWN")

    def reverse_flash(self):
        self.tft.inversion_mode(0)
        time.sleep_ms(100)
        self.tft.inversion_mode(1)

    def refresh(self):
        pass

    def fill(self, color565=0):
        self.tft.fill(color565)

    def sprite(self, sprite, x, y, width, height, color, bg_color, sprite_buffer=None):
        collect = False
        if sprite_buffer is None:
            sprite_buffer = bytearray(width * height * self.color_bytes)
            collect = True
        self.tft.map_bitarray_to_rgb565(sprite, sprite_buffer, width, color, bg_color)
        self.tft.blit_buffer(sprite_buffer, x, y, width, height)
        if collect:
            del sprite
            gc.collect()

    def do_event(self, touch):
        if self.on_event:
            self.on_event(touch)

    def tick(self):
        pass

