"""
High level GUI Manager for Walt Basic

Very same code used in simulator and on hardware

# Copyright (C) 2020 Angainor
"""

import time
import logos
import gc
from os import statvfs, uname
import colors_565_basic_1 as colors
import life

try:
    import urandom as random
except:
    import random

from math import sqrt

MENU_SIZE = 48
MENU_SLOTS = [
    (24, 26), (24+54, 26), (24+54*2, 26), (24+54*3, 26),
    (24, 26+54), (24+54, 26+54), (24+54*2, 26+54), (24+54*3, 26+54)
    ]

PIN_SIZE = (16, 32)
PIN_SLOTS = [(8, 26), (8+(16 + 8)*1, 26), (8+(16 + 8)*2, 26),  (8+(16 + 8)*3, 26),  (8+(16 + 8)*4, 26),  (8+(16 + 8)*5, 26),  (8+(16 + 8)*6, 26),  (8+(16 + 8)*7, 26), (8+(16 + 8)*8, 26),
(8, 64), (8+(16 + 8)*1, 64), (8+(16 + 8)*2, 64),  (8+(16 + 8)*3, 64),  (8+(16 + 8)*4, 64),  (8+(16 + 8)*5, 64),  (8+(16 + 8)*6, 64),  (8+(16 + 8)*7, 64), (8+(16 + 8)*8, 64),
             (8+(16 + 8)*8, 64+32)
]

A2COLORS = [colors.A0, colors.A1, colors.A2]


class DisplayManager():
    """High level GUI manager with dedicated primitives
    """

    def __init__(self, ui, engine):
        self.engine = engine
        self.engine.parent = self
        self.ui = ui
        if self.ui.hwui.emulated:
            print("LOG: Emulated display")
        ui.on_event = self.on_event
        self.until = []
        
        self.active = False
        self.result = None
        self.menu_index = 0
        # To be loaded from some config
        self.menu_items = [(logos.bluetooth_icon16x16, "BLE", self.engine.core.toggle_ble),
                           (logos.wifi_icon16x16, "WIFI", self.engine.core.toggle_wifi),
                           (self.lock_logo, self.lock_text, self.lockunlock),
                           (logos.sun_icon16x16, "Contrast", self.engine.core.toggle_contrast),
                           (logos.NYZO_46x46, "Nyzo", None),
                           (logos.IDENA_46x46, "Idena", None),
                           (logos.tool_icon16x16, "?", self.life_screen),
                           (logos.speak_icon16x16, "Info", self.info)]
        self.pin_index = 0
        self.anim_index = 20
        self.anim_index2 = 0
        self.anim_direction = 1
        # Not needed for current animation - TODO: config
        self.anim_buffer = None  # bytearray(16 * 16 * self.ui.hwui.color_bytes)
        self.sprite_buffer = None
        self.command_buffer = ""
        self.screen = "boot"
        self.life = None  # Generalize, self.app?

    def lock_logo(self):
        if self.engine.locked:
            return logos.lock_open_icon16x16
        else:
            return logos.lock_closed_icon16x16

    def lock_text(self):
        if self.engine.locked:
            return "Unlock"
        else:
            return "Lock"

    def color_icon_if(self, on):
        return colors.SELECTED if on else colors.BG

    def on_event(self, touch):
        # print("DM Event", touch)
        self.result = touch
        if touch in self.until:
            self.active = False

    def life_screen(self):
        self.ui.clear()
        self.life = life.Life()
        self.screen = "life"
        self.status_bar(self.sprite_buffer)
        self.buttons2(logos.arrow_right_icon16x16, colors.SELECTED, logos.check_icon16x16,
                      colors.SELECTED, self.sprite_buffer)

        self.active = True
        res = self.run_until(["UP", "DOWN"])
        self.life.clear()
        del self.life
        self.life = None
        gc.collect()

    def animate_life(self):
        # compute
        self.life.computeCA()
        # draw
        changed = 0
        for x in range(1, life.GRIDX - 1):
            for y in range(1, life.GRIDY -1):
                if self.life.grid[x][y] != self.life.newgrid[x][y]:
                    changed += 1
                    if self.life.newgrid[x][y] == 1:
                        color = colors.NYZO
                    else:
                        color = colors.BG
                    self.ui.fill_rect(life.CELLXY * x, 20 + life.CELLXY * y,
                                      life.CELLXY, life.CELLXY, color)
        if changed <5:
            self.life.initGrid()

        # copy to current gen
        self.life.nextGen()

    def info(self):
        print("LOG: Info")
        stat = statvfs('/')  # Internal Flash
        blocksize = stat[0]
        fragsize = stat[1]
        fragfs = stat[2]
        freeblocks = stat[3]
        fs_size = fragfs * fragsize / 1024  # In KB
        free_size = blocksize * freeblocks / 1024  # In Kb
        # Show FS usage
        print("LOG: FS: %2i/%2i Kb" % (fs_size - free_size, fs_size))  # default 2MB flash, too much. MBFS instead of VFS?
        try:
            print("LOG: RAM: Alloc {}/Free {}".format(gc.mem_alloc(), gc.mem_free()))
        except:
            pass
        self.ui.clear()
        self.screen = "info"
        self.status_bar(self.sprite_buffer)
        self.status_text("Info")
        self.buttons2(logos.arrow_right_icon16x16, colors.SELECTED, logos.check_icon16x16,
                      colors.SELECTED, self.sprite_buffer)
        y = 30
        self.ui.text(8, uname()[4], 8, y)
        # print(uname()) # (sysname='esp32', nodename='esp32', release='1.16.0', version='v1.16 on 2021-06-20', machine='WALT Basic with ESP32')
        y+=16
        self.ui.text(8, "MPY Ver {}".format(uname()[2]), 8, y)
        y+=16
        self.ui.text(8, "Engine v{}".format(self.engine.version), 8, y)            
        # print(uname())
        y+=16
        self.ui.text(8, "", 8, y)
        y+=16
        self.ui.text(8, "FS: %2i/%2i Kb" % (fs_size - free_size, fs_size), 8, y)
        try:
            y+=16
            self.ui.text(8, "RAM Alloc {}/Free {}".format(gc.mem_alloc(), gc.mem_free()), 8, y)
        except:
            pass
          
        self.active = True
        res = self.run_until(["UP", "DOWN"])
        gc.collect()            

    def animate1(self):
        # ready copied buffer? no need to copy everytime, but means low level thing
        self.ui.sprite(logos.sun_icon16x16, 0, self.anim_index, 16, 16, colors.YES, colors.BG,
                       self.anim_buffer)
        self.anim_index += self.anim_direction
        if self.anim_index > 135 - 20 - 16 or self.anim_index < 20:
            self.anim_direction = -self.anim_direction

    def cmd_ping(self):
        print("W:PONG")

    def cmd_version(self):
        print("W:VERSION:{}".format(self.engine.version))

    def animate(self):
        # todo: modularize, call needed methods depending on current screen
        if self.screen in ["main_menu"]:
            # useless "it's alive" animation
            xoffset = 2
            if self.ui.hwui.orientation == 1:
                xoffset = 240 - 20 + 2
            self.anim_index += 1
            if self.anim_index > 10:
                if random.randint(0, 1) == 1:
                    return
                col = random.randint(0, 1)
                line = random.randint(0, 4)
                color = A2COLORS[random.randint(0, 2)]
                # 135-20-20 = 95 = 19*5
                self.ui.fill_rect(xoffset + 10 * col, 20 + 2 + 19 * line, 8, 17, color)
                self.anim_index = 0

        if self.screen == "main_menu":
            # animate menu cursor
            self.anim_index2 = (self.anim_index2 + 1 ) % (MENU_SIZE * 2)
            slot = MENU_SLOTS[self.menu_index]
            xoffset = 0
            if self.ui.hwui.orientation == 1:
                xoffset = - 20
            x = xoffset + slot[0]
            y = slot[1]
            color2 = colors.SELECTED
            color1 = colors.STATUS_BG
            if self.anim_index2 < MENU_SIZE:
                i = self.anim_index2
            else:
                i = self.anim_index2 - MENU_SIZE
                color2, color1 = color1, color2
            self.ui.vline(x, y, MENU_SIZE - i, color2)
            self.ui.vline(x, y + MENU_SIZE - i, i, color1)
            self.ui.vline(x + MENU_SIZE -1, y, i, color1)
            self.ui.vline(x + MENU_SIZE -1, y + i, MENU_SIZE - i, color2)
            self.ui.hline(x, y , i, color2)
            self.ui.hline(x + i+0, y , MENU_SIZE - i - 1, color1)
            self.ui.hline(x, y + MENU_SIZE - 1, MENU_SIZE - i - 1, color1)
            self.ui.hline(x + 0 + MENU_SIZE - i, y + MENU_SIZE - 1, i, color2)

        if self.screen in ["unlock"]:
            # animate select cursor
            self.anim_index2 = (self.anim_index2 + 1) % 100
            slot = PIN_SLOTS[self.pin_index]
            color = self.ui.c565fade(colors.SELECTED, self.anim_index2)
            self.ui.sprite(logos.select_icon16x3, slot[0], slot[1]+30, 16, 3, color, colors.BG, self.sprite_buffer)

        if self.screen == "life":
            self.animate_life()

    def animate_init(self):
        xoffset = 2
        if self.ui.hwui.orientation == 1:
            xoffset = 240 - 20 + 2
        for col in range(2):
            for line in range(5):
                self.ui.fill_rect(xoffset + 10 * col, 20 + 2 + 19 * line, 8, 17, A2COLORS[0])

    def run_until(self, until):
        self.until = until
        while self.active:
            self.engine.tick()
            self.ui.tick()
            self.animate()
            # TODO: sleep_ms if exists (micropy)
            time.sleep(0.01)
        return self.result

    def run(self):
        self.welcome_screen()
        time.sleep(2)
        self.main_menu_screen()

    def lockunlock(self):
        if self.engine.locked:
            print("Unlock")
            pin = self.unlock_screen()
            self.engine.unlock(pin)
        else:
            print("Lock")
            self.engine.lock()

    def unlock_screen(self):
        def set_pin_index(index):
            slot = PIN_SLOTS[self.pin_index]
            self.ui.sprite(logos.select_icon16x3, slot[0], slot[1] + 30, 16, 3, colors.BG, colors.BG,
                           self.sprite_buffer)
            self.pin_index = index

        self.ui.clear()
        self.screen = "unlock"
        self.status_bar(self.sprite_buffer)
        self.buttons2(logos.arrow_right_icon16x16, colors.SELECTED, logos.check_icon16x16,
                      colors.SELECTED, self.sprite_buffer)
        color = colors.ICON
        y = 16 + 10
        x = 8
        self.ui.text(16, "0", x, y, color, colors.BG)
        self.ui.text(16, "1", x + 16 + 8, y, color, colors.BG)
        self.ui.text(16, "2", x + (16 + 8) * 2, y, color, colors.BG)
        self.ui.text(16, "3", x + (16 + 8) * 3, y, color, colors.BG)
        self.ui.text(16, "4", x + (16 + 8) * 4, y, color, colors.BG)
        self.ui.text(16, "5", x + (16 + 8) * 5, y, color, colors.BG)
        self.ui.text(16, "6", x + (16 + 8) * 6, y, color, colors.BG)
        self.ui.text(16, "7", x + (16 + 8) * 7, y, color, colors.BG)
        self.ui.text(16, "<", x + (16 + 8) * 8, y, color, colors.BG)
        # self.ui.sprite(logos.cancel_icon16x16, x + (16 + 8) * 8, y+7, 16, 16, color, colors.BG, self.sprite_buffer)
        y= 16 + 16 + 32
        self.ui.text(16, "8", x + (16 + 8) * 0, y, color, colors.BG)
        self.ui.text(16, "9", x + (16 + 8) * 1, y, color, colors.BG)
        self.ui.text(16, "A", x + (16 + 8) * 2, y, color, colors.BG)
        self.ui.text(16, "B", x + (16 + 8) * 3, y, color, colors.BG)
        self.ui.text(16, "C", x + (16 + 8) * 4, y, color, colors.BG)
        self.ui.text(16, "D", x + (16 + 8) * 5, y, color, colors.BG)
        self.ui.text(16, "E", x + (16 + 8) * 6, y, color, colors.BG)
        self.ui.text(16, "F", x + (16 + 8) * 7, y, color, colors.BG)
        #self.ui.text(16, ">", x + (16 + 8) * 8, y, color, colors.BG)
        self.ui.sprite(logos.check_icon16x16, x + (16 + 8) * 8, y + 7,  16, 16, color, colors.BG, self.sprite_buffer)

        self.ui.sprite(logos.cancel_icon16x16, x + (16 + 8) * 8, y + 7 + 32, 16, 16, color, colors.BG, self.sprite_buffer)
        #self.ui.sprite(logos.check_icon16x16, x + (16 + 8) * 8, y+7+32, 16, 16, color, colors.BG, self.sprite_buffer)

        self.ui.text(8, ">", x + (16 + 8) * 0, 16 + 32 + 16 + 32 + 8, colors.STATUS_BG, colors.BG)
        # self.pin_index = 0
        set_pin_index(random.randint(0, len(PIN_SLOTS) -1))

        """
        for num, slot in enumerate(PIN_SLOTS):
            self.ui.rect(slot[0], slot[1], PIN_SIZE[0], PIN_SIZE[1], colors.SELECTED)
        """
        pin = ''
        texts =('0', '1', '2', '3', '4' ,'5', '6', '7', '<',
                '8', '9', 'A', 'B', 'C', 'D', 'E', 'F',  'VAL', 'CAN')
        while True:
            self.active = True
            res = self.run_until(["UP", "DOWN"])
            if res == "UP":
                slot = PIN_SLOTS[self.pin_index]
                self.ui.sprite(logos.select_icon16x3, slot[0], slot[1] + 30, 16, 3, colors.BG, colors.BG,
                               self.sprite_buffer)
                self.pin_index += 1
                if self.pin_index >= len(PIN_SLOTS):
                    self.pin_index = 0
            elif res == "DOWN":
                text = texts[self.pin_index]
                if text == "<":
                    pin = pin[:-1]
                elif text == "CAN":
                    return ""
                elif text == "VAL":
                    return pin
                else:
                    pin += text
                self.ui.text(8, "{} ".format(pin), 10 + x + (16 + 8) * 0, 16 + 32 + 16 + 32 + 8, colors.TEXT2, colors.BG)
                set_pin_index(random.randint(0, len(PIN_SLOTS) - 1))

                #return pin

    def welcome_screen(self):
        self.ui.clear()
        self.ui.text(16, "Walt Basic", -1, 16 + 64, colors.TEXT2)
        self.ui.text(8, "v" + self.engine.version, -1, 135 - 20, colors.TEXT2)
        sprite_buffer = bytearray(64 * 64 * self.ui.hwui.color_bytes)
        self.ui.sprite(logos.WALT_64x64, self.ui.hwui.width // 2 - 32, 14, 64, 64, colors.WALT, colors.BG, sprite_buffer)
        del sprite_buffer
        gc.collect()
        
    def status_bar(self, sprite_buffer=None):
        collect = False
        if sprite_buffer is None:
            sprite_buffer = bytearray(16 * 16 * self.ui.hwui.color_bytes)
            collect = True
        xoffset = 20
        xoffseticons = 220
        if self.ui.hwui.orientation == 1:
            xoffset = 0
            xoffseticons = 215  # right of icons
        self.ui.fill_rect(xoffset, 0, 220, 20, colors.STATUS_BG)
        if self.engine.locked:
            self.ui.sprite(logos.lock_closed_icon16x16, xoffset + xoffseticons - 20, 3, 16, 16,
                           colors.SELECTED, colors.STATUS_BG, sprite_buffer)
        else:
            self.ui.sprite(logos.lock_open_icon16x16, xoffset + xoffseticons - 20, 3, 16, 16,
                           colors.SELECTED, colors.STATUS_BG, sprite_buffer)
        self.ui.sprite(logos.wifi_icon16x16, xoffset + xoffseticons - 20 * 2, 4, 16, 16, self.color_icon_if(self.engine.core.WIFI),
                       colors.STATUS_BG, sprite_buffer)
        self.ui.sprite(logos.bluetooth_icon16x16, xoffset + xoffseticons - 20 * 3, 2, 16, 16, self.color_icon_if(self.engine.core.BLE),
                       colors.STATUS_BG, sprite_buffer)
        if collect:
            del sprite_buffer
            gc.collect()

    def buttons2(self, sprite_up, color_up, sprite_down, color_down, sprite_buffer=None):
        xoffset = 0
        if self.ui.hwui.orientation == 1:
            xoffset = 240-20
        if False:
            self.ui.rect(xoffset, 0, 20, 20, colors.SELECTED)
            self.ui.rect(xoffset, 135 - 20, 20, 20, colors.SELECTED)
        collect = False
        if sprite_buffer is None:
            sprite_buffer = bytearray(16 * 16 * self.ui.hwui.color_bytes)
            collect = True
        self.ui.sprite(sprite_up, xoffset + 2, 2, 16, 16, color_up, colors.BG, sprite_buffer)
        self.ui.sprite(sprite_down, xoffset + 2, 135 - 16 - 2, 16, 16, color_down, colors.BG, sprite_buffer)
        if collect:
            del sprite_buffer
            gc.collect()

    def status_text(self, text):
        xtextoffset = 24
        if self.ui.hwui.orientation == 1:
            xtextoffset = 4
        while len(text) < 8:
            text = text + " "
        self.ui.text(8, text[:8], xtextoffset, 4, colors.TEXT2, colors.STATUS_BG)

    def main_menu_screen(self):
        self.screen = "main_menu"
        self.sprite_buffer = bytearray(64*64*self.ui.hwui.color_bytes)  # Largest possible buffer
        size = MENU_SIZE
        redraw = True  # redraw all icons?
        xoffset = 0
        if self.ui.hwui.orientation == 1:
            xoffset = -20
        while True:
            if redraw:
                self.ui.clear()
                self.animate_init()
                self.buttons2(logos.arrow_right_icon16x16, colors.SELECTED, logos.check_icon16x16,
                              colors.SELECTED, self.sprite_buffer)
            self.status_bar(self.sprite_buffer)
            for position, slot in enumerate(MENU_SLOTS):
                item = self.menu_items[position]  # TODO: add page
                logo = item[0]
                if callable(logo):
                    logo = item[0]()
                # print("logo", logo, type(logo))
                text = item[1]
                if callable(text):
                    text = item[1]()
                width = int(sqrt(len(logo) * 8))
                offset = 0
                if width < 46:
                    offset = (46 - width) // 2
                if position == self.menu_index:
                    # self.ui.rect(xoffset + slot[0], slot[1], size, size, colors.SELECTED)  # Taken care by animation
                    # self.ui.rect(xoffset + slot[0]-1, slot[1]-1, size+2, size+2, colors.STATUS_BG)

                    if redraw:
                        self.ui.sprite(logo, xoffset + slot[0] + 2 + offset, slot[1] + 2 + offset,
                                       width, width, colors.ICON, colors.BG, self.sprite_buffer)
                    self.status_text(text)

                else:
                    self.ui.rect(xoffset + slot[0], slot[1], size, size, colors.BG)
                    # lower saturation?
                    if redraw:
                        self.ui.sprite(logo, xoffset + slot[0] + 2 + offset, slot[1] + 2 + offset,
                                       width, width, colors.ICON, colors.BG, self.sprite_buffer)
            self.active = True
            redraw = False  # only set True again if page changes
            res = self.run_until(["UP", "DOWN"])
            if res == "UP":
                self.menu_index += 1
                if self.menu_index >= len(MENU_SLOTS):
                    self.menu_index = 0
            elif res == "DOWN":
                # print("Click", self.menu_index)
                item_action = self.menu_items[self.menu_index][2]
                if item_action:
                    item_action()
                    """
                    try:
                        item_action()
                    except Exception as e:
                        print("E: {}".format(e))
                    """
                    redraw = True
                    gc.collect()
                    self.screen = "main_menu"
        del self.sprite_buffer
        gc.collect()
        return self.menu_index
        
    def confirm_tx_screen(self, coin, amount, recipient, extra):
        self.active = True
        self.ui.clear()
        sprite_buffer = bytearray(64*64*self.ui.hwui.color_bytes)

        self.ui.sprite(logos.check_icon16x16, 2, 0, 16, 16, colors.YES, colors.BG, sprite_buffer )
        self.ui.sprite(logos.cancel_icon16x16, 2, 118, 16, 16, colors.NO, colors.BG, sprite_buffer )
        self.ui.sprite(logos.NYZO_46x46, 182, 14, 46, 46, colors.NYZO, colors.BG, sprite_buffer )

        self.ui.text(16, "Confirm", 32, 16, colors.TEXT2, sprite_buffer=sprite_buffer)
        self.ui.text(8, "{} {} to".format(amount, coin), 32, 64, sprite_buffer=sprite_buffer)
        self.ui.text(8, recipient, 32, 64 + 16 + 4, sprite_buffer=sprite_buffer)
        while self.active:
            self.ui.tick()
            time.sleep(0.1)
        del sprite_buffer
        gc.collect()
        
        return self.result
        
        
        
        
