ST7789_MOD_DIR := $(USERMOD_DIR)
SRC_USERMOD += $(addprefix $(ST7789_MOD_DIR)/, \
	st7789.c \
)
CFLAGS_USERMOD += -I$(ST7789_MOD_DIR) -DMODULE_ST7789_ENABLED=1
CFLAGS_USERMOD += -DEXPOSE_EXTRA_METHODS=1

