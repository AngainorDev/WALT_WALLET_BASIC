# SPDX-License-Identifier: LGPL-3.0-or-later

# Loosely based on code from
# Copyright (C) 2020 Daniel Thompson
# Copyright (C) 2020 Angainor

# Only used in desktop python context

""" Simulated ST7789 display and CST816S touchscreen. """

import sys
import sdl2
import sdl2.ext

CASET = 0x2a
RASET = 0x2b
RAMWR = 0x2c


"""
RED = 0xF800
BLACK  = 0x0000
BLUE   = 0x001F    
GREEN =  0x07E0
CYAN   = 0x07FF
MAGENTA = 0xF81F
YELLOW  = 0xFFE0
WHITE  = 0xFFFF
DARK_GRAY = 0x39E7
LIGHT_GRAY = 0x9CF3
"""
COLORBYTES = 3  # 2 for hardware rgb 565, 3 for simulated RGB
EMULATED = True

# This is emulated device specific
WIDTH = 240
HEIGHT = 135

SKIN = {
    'fname' : 'res/left_skin.png',
    'size' : (437, 222),
    'offset' : (143,40)
}

BUTTONS = {
    "UP": ((35, 27), (82, 64)),
    "DOWN": ((35, 156), (82, 192))
    }
# End

ON_EVENT = None

# Move to displayManager
MENU_SIZE = 48
MENU_SLOTS = [
    (24, 26), (24+54, 26), (24+54*2, 26), (24+54*3, 26),
    (24, 26+54), (24+54, 26+54), (24+54*2, 26+54), (24+54*3, 26+54)
    ]


class ST7789Sim(object):
    def __init__(self):
        pass
        
    def c565topixel(self, color565):
        r = color565 & 0b1111100000000000
        g = color565 & 0b0000011111100000
        b = color565 & 0b0000000000011111
        r = r >> 8
        g = g >> 3
        b = b << 3
        # print(r,g,b)
        return (r, g, b)
        
    def fill(self, color565):
        sdl2.ext.fill(windowsurface, self.c565topixel(color565), (SKIN['adjust'][0], SKIN['adjust'][1], WIDTH, HEIGHT))
        window.refresh()

    def filled_rect(self, x, y, w, h, color565):
        sdl2.ext.fill(windowsurface, self.c565topixel(color565), (SKIN['adjust'][0]+x, SKIN['adjust'][1]+y, w, h))
        window.refresh()
        
    def map_bitarray_to_rgb565(self, bitarray, buffer, width, color, bg_color):
        row_pos = 0
        buffer_index = 0
        color = self.c565topixel(color)
        bg_color = self.c565topixel(bg_color)  
        length = len(bitarray)
        for i in range(length):
            byte = bitarray[i]
            for bi in reversed(range(8)):
                b = byte & (1 << bi)
                cur_color = color if b else bg_color
                buffer[buffer_index] = cur_color[0]
                buffer_index += 1
                buffer[buffer_index] = cur_color[1]
                buffer_index += 1
                buffer[buffer_index] = cur_color[2]
                buffer_index += 1

                row_pos+= 1
                if row_pos >= width:
                    row_pos = 0
                    break
                    
    def blit_buffer(self, sprite,x, y, w, h):
        pixelview = sdl2.ext.pixels2d(windowsurface)    
        index = 0 
        for i in range(h):
            for j in range(w):
                pixelview[x+j + SKIN['adjust'][0], y+i + SKIN['adjust'][1]] = sprite[index]*256*256+sprite[index+1]*256+sprite[index+2]
                index += 3
        del pixelview
        window.refresh()
        
    def text(self, font, text, x, y, color, bg_color):
        pos = 0
        mv = memoryview(font._FONT)
        sprite = bytearray(font.WIDTH*font.HEIGHT*3)
        for char in text:
            if ord(char) < font.FIRST:
                continue
            if ord(char) > font.LAST:
                continue
            index = (ord(char) - font.FIRST)*(font.WIDTH*font.HEIGHT)//8
            # index = 0
            self.map_bitarray_to_rgb565(mv[index:index+(font.WIDTH*font.HEIGHT)//8], sprite, font.WIDTH, color, bg_color)
            self.blit_buffer(sprite, x+pos*font.WIDTH, y, font.WIDTH, font.HEIGHT)
            pos += 1
                    
    def rect(self, x, y, w, h, color565):
        x += SKIN['adjust'][0]
        y += SKIN['adjust'][1]
        lines = [x,y,x+w,y]
        lines += [x+w,y,x+w,y+h]
        lines += [x+w,y+h,x, y+h]
        lines += [x, y+h, x,y]
        #print(lines)
        sdl2.ext.line(windowsurface, self.c565topixel(color565), lines)
        window.refresh()

# Derive some extra values for padding the display
SKIN['left_pad'] = 9
SKIN['right_pad'] = SKIN['left_pad']
SKIN['top_pad'] = 3
SKIN['bottom_pad'] = 3
SKIN['window'] = (SKIN['size'][0] + SKIN['left_pad'] + SKIN['right_pad'],
                  SKIN['size'][1] + SKIN['top_pad'] + SKIN['bottom_pad'])
SKIN['adjust'] = (SKIN['offset'][0] + SKIN['left_pad'],
                  SKIN['offset'][1] + SKIN['top_pad'])

sdl2.ext.init()
window = sdl2.ext.Window("Walt Basic", size=SKIN['window'])
window.show()
windowsurface = window.get_surface()
sdl2.ext.fill(windowsurface, (0xff, 0xff, 0xff))
skin = sdl2.ext.load_image(SKIN['fname'])
sdl2.SDL_BlitSurface(skin, None, windowsurface, sdl2.SDL_Rect(
        SKIN['left_pad'], SKIN['top_pad'], SKIN['size'][0], SKIN['size'][1]))
sdl2.SDL_FreeSurface(skin)
window.refresh()

tft = ST7789Sim()


def do_event(touch):
    if ON_EVENT:
        ON_EVENT(touch)


def tick():
    events = sdl2.ext.get_events()
    for event in events:
        if event.type == sdl2.SDL_QUIT:
            sdl2.ext.quit()
            sys.exit(0)
        elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
            print("Mouse Down", event.button.x, event.button.y)
            #i2c_cst816s_sim.handle_mousebuttondown(event.button, pins)
        elif event.type == sdl2.SDL_MOUSEBUTTONUP:
            #i2c_cst816s_sim.handle_mousebuttonup(event.button, pins)
            print("Mouse Up", event.button.x, event.button.y)    
            for button in BUTTONS:
                limits = BUTTONS[button]
                if event.button.x >= limits[0][0] and event.button.x <= limits[1][0] \
                        and event.button.y >= limits[0][1] and event.button.y <= limits[1][1]:
                    do_event(button)     
        elif event.type == sdl2.SDL_KEYDOWN:
            if event.key.keysym.sym == sdl2.SDLK_TAB:
                pass
                # pins['BUTTON'].value(0)
                # do_event("TAB")
            else:
                #i2c_cst816s_sim.handle_key(event.key, pins)
                print("keydown", event.key.keysym.sym)     
        elif event.type == sdl2.SDL_KEYUP:
            if event.key.keysym.sym == sdl2.SDLK_TAB:
                #pins['BUTTON'].value(1)
                do_event("TAB")
            elif event.key.keysym.sym == sdl2.SDLK_DOWN:
                do_event("DOWN")
            elif event.key.keysym.sym == sdl2.SDLK_UP:
                do_event("UP")
            elif event.key.keysym.sym == 13:
                do_event("ENTER")
            elif event.key.keysym.sym == 27:
                do_event("ESC")
            print("keyup", event.key.keysym.sym)        
        else:
            #print(event)
            pass
    window.refresh()
