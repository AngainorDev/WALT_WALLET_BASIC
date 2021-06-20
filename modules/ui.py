# Generic UI Interface
# hardware inpedendant

import gc
import colors_565_basic_1 as colors


class UI(object):
    def __init__(self, hwui):
        self.hwui = hwui
        self.on_event = None
        self.fill = hwui.fill
        self.sprite = hwui.sprite
        self.fill_rect = hwui.fill_rect
        self.rect = hwui.rect
        self.line = hwui.line
        self.vline = hwui.vline
        self.hline = hwui.hline
        self.tick = self.hwui.tick
        self.reverse_flash = self.hwui.reverse_flash

    @property
    def on_event(self):
        return self.on_event

    @on_event.setter
    def on_event(self, handler):
        self.hwui.on_event = handler

    def c565fade(self, color565, percent):
        # dim a rgb565 color. 100 = full, 0 = black
        r = color565 & 0b1111100000000000
        g = color565 & 0b0000011111100000
        b = color565 & 0b0000000000011111
        if percent == 0:
            return 0
        r = (r >> 8) * 100 // percent
        g = (g >> 3) * 100 // percent
        b = (b << 3) * 100 // percent
        return (r*31//255) << 11 | (g*63//255) << 5 | (b*31//255)

    def clear(self):
        self.hwui.fill(colors.BG)

    def text(self, size, text, x, y, color=None, bg_color=None, sprite_buffer=None):
        collect = False
        if color is None:
            color = colors.TEXT
        if bg_color is None:
            bg_color = colors.BG
        if size == 16:
            import vga1_16x32 as font
        elif size == 8:
            import vga1_8x16 as font
        else:
            size = 8
            import vga1_8x16 as font
        if x == -1:
            # center
            width = len(text) * size
            x = (self.hwui.width - width) // 2
        if y == -1:
            # center
            height = 2 * size
            y = (self.hwui.height - height) // 2
        # self.tft.text(font, text, x, y, color, bg_color)
        pos = 0
        mv = memoryview(font._FONT)
        # for st7789, could use the text method from the c impl. really way faster for our usecase?
        if sprite_buffer is None:
            sprite_buffer = bytearray(font.WIDTH * font.HEIGHT * self.hwui.color_bytes)
            collect = True
        for char in text:
            if ord(char) < font.FIRST:
                continue
            if ord(char) > font.LAST:
                continue
            index = (ord(char) - font.FIRST) * (font.WIDTH * font.HEIGHT) // 8
            self.hwui.sprite(mv[index:index + (font.WIDTH * font.HEIGHT) // 8],
                             x + pos * font.WIDTH, y, font.WIDTH, font.HEIGHT,
                             color, bg_color, sprite_buffer)
            pos += 1
        if collect:
            del sprite_buffer
            gc.collect()