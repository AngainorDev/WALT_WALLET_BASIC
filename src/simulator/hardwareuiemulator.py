# Hardware interface layer.
# Emulator
# Close to the hardware, only basic primitives.

# SPDX-License-Identifier: LGPL-3.0-or-later
# Copyright (C) 2020 Daniel Thompson
# Copyright (C) 2020 Angainor

""" Simulated rgb565 display and hardware buttons"""

import sys
import sdl2
import sdl2.ext
import gc
import os
import json


def c565topixel(color565):
    r = color565 & 0b1111100000000000
    g = color565 & 0b0000011111100000
    b = color565 & 0b0000000000011111
    r = r >> 8
    g = g >> 3
    b = b << 3
    return r, g, b


class HardwareUIEmulator(object):

    def __init__(self, name="basic3"):
        self.emulated = True
        self.color_bytes = 3  # 2 for hardware rgb 565, 3 for simulated RGB
        dir_path = os.path.dirname(os.path.realpath(__file__))
        config_file = os.path.join(dir_path,"{}.json".format(name))
        if not os.path.isfile(config_file):
            raise("Config file not found")
        with open(config_file) as fp:
            config = json.load(fp)
        self.width = config["width"]
        self.orientation = config["orientation"]
        self.height = config["height"]
        self.buttons = config["buttons"]
        # Derive some extra values for padding the display
        self.skin = config["skin"]
        self.skin['left_pad'] = 9
        self.skin['right_pad'] = self.skin['left_pad']
        self.skin['top_pad'] = 3
        self.skin['bottom_pad'] = 3
        self.skin['window'] = (self.skin['size'][0] + self.skin['left_pad'] + self.skin['right_pad'],
                          self.skin['size'][1] + self.skin['top_pad'] + self.skin['bottom_pad'])
        self.skin['adjust'] = (self.skin['offset'][0] + self.skin['left_pad'],
                          self.skin['offset'][1] + self.skin['top_pad'])
        sdl2.ext.init()
        self.window = sdl2.ext.Window(config["name"], size=self.skin['window'])
        self.window.show()
        self.windowsurface = self.window.get_surface()
        sdl2.ext.fill(self.windowsurface, (0xff, 0xff, 0xff))
        skin_image = sdl2.ext.load_image(self.skin['fname'])
        sdl2.SDL_BlitSurface(skin_image, None, self.windowsurface,
                             sdl2.SDL_Rect(self.skin['left_pad'], self.skin['top_pad'],
                                           self.skin['size'][0], self.skin['size'][1]))
        sdl2.SDL_FreeSurface(skin_image)
        self.on_event = None
        self.refresh()

    def reverse_flash(self):
        print("EMUL: reverse_flash")

    def refresh(self):
        self.window.refresh()

    def fill(self, color565=0):
        sdl2.ext.fill(self.windowsurface, c565topixel(color565),
                      (self.skin['adjust'][0], self.skin['adjust'][1], self.width, self.height))
        self.refresh()

    def fill_rect(self, x, y, w, h, color565):
        sdl2.ext.fill(self.windowsurface, c565topixel(color565),
                      (self.skin['adjust'][0] + x, self.skin['adjust'][1] + y, w, h))
        self.refresh()

    def _map_bitarray_to_rgb565(self, bitarray, buffer, width, color, bg_color):
        row_pos = 0
        buffer_index = 0
        color = c565topixel(color)
        bg_color = c565topixel(bg_color)
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

                row_pos += 1
                if row_pos >= width:
                    row_pos = 0
                    break

    def _blit_buffer(self, sprite, x, y, w, h):
        pixelview = sdl2.ext.pixels2d(self.windowsurface)
        index = 0
        for i in range(h):
            for j in range(w):
                pixelview[x + j + self.skin['adjust'][0], y + i + self.skin['adjust'][1]] = \
                    sprite[index] * 256 * 256 + sprite[index + 1] * 256 + sprite[index + 2]
                index += 3
        del pixelview
        self.refresh()

    def sprite(self, sprite, x, y, width, height, color, bg_color, sprite_buffer=None):
        collect = False
        if sprite_buffer is None:
            sprite_buffer = bytearray(width * height * self.color_bytes)
            collect = True
        self._map_bitarray_to_rgb565(sprite, sprite_buffer, width, color, bg_color)
        self._blit_buffer(sprite_buffer, x, y, width, height)
        if collect:
            del sprite
            gc.collect()

    def line(self, x, y, x2, y2, color565):
        x += self.skin['adjust'][0]
        y += self.skin['adjust'][1]
        x2 += self.skin['adjust'][0]
        y2 += self.skin['adjust'][1]
        lines = [x, y, x2, y2]
        sdl2.ext.line(self.windowsurface, c565topixel(color565), lines)
        self.refresh()

    def hline(self, x, y, w, color565):
        if w == 0:
            return
        self.line(x, y, x+w, y, color565)

    def vline(self, x, y, w, color565):
        if w == 0:
            return
        self.line(x, y, x, y+w, color565)

    def rect(self, x, y, w, h, color565):
        x += self.skin['adjust'][0]
        y += self.skin['adjust'][1]
        lines = [x, y, x + w-1, y]
        lines += [x + w-1, y, x + w-1, y + h]
        lines += [x + w, y + h-1, x, y + h-1]
        lines += [x, y + h, x, y]
        sdl2.ext.line(self.windowsurface, c565topixel(color565), lines)
        self.refresh()

    def do_event(self, touch):
        if self.on_event:
            self.on_event(touch)

    def tick(self):
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                sdl2.ext.quit()
                sys.exit(0)
            elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                print("Mouse Down", event.button.x, event.button.y)
            elif event.type == sdl2.SDL_MOUSEBUTTONUP:
                print("Mouse Up", event.button.x, event.button.y)
                for button in self.buttons:
                    limits = self.buttons[button]
                    if event.button.x >= limits[0][0] and event.button.x <= limits[1][0] \
                            and event.button.y >= limits[0][1] and event.button.y <= limits[1][1]:
                        self.do_event(button)
            elif event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_TAB:
                    pass
                else:
                    print("keydown", event.key.keysym.sym)
            elif event.type == sdl2.SDL_KEYUP:
                if event.key.keysym.sym == sdl2.SDLK_TAB:
                    # pins['BUTTON'].value(1)
                    self.do_event("TAB")
                elif event.key.keysym.sym == sdl2.SDLK_DOWN:
                    self.do_event("DOWN")
                elif event.key.keysym.sym == sdl2.SDLK_UP:
                    self.do_event("UP")
                elif event.key.keysym.sym == 13:
                    self.do_event("ENTER")
                elif event.key.keysym.sym == 27:
                    self.do_event("ESC")
                print("keyup", event.key.keysym.sym)
            else:
                # print(event)
                pass
        # screen.refresh()
