set(SDKCONFIG_DEFAULTS
    boards/sdkconfig.base
    boards/sdkconfig.ble
    # boards/sdkconfig.240mhz
    boards/WALT_WALLET_BASIC/sdkconfig.walt
)

if(NOT MICROPY_FROZEN_MANIFEST)
    set(MICROPY_FROZEN_MANIFEST ${MICROPY_PORT_DIR}/boards/WALT_WALLET_BASIC/manifest.py)
endif()

set(USER_C_MODULES ${MICROPY_PORT_DIR}/boards/WALT_WALLET_BASIC/c-modules/micropython.cmake)
set(CFLAGS_EXTRA -DMODULE_TREZORCRYPTO_ENABLED=1)
