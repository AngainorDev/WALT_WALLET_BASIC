# Create an INTERFACE library for our C module.
add_library(usermod_modtcc INTERFACE)

# Add our source files to the lib
target_sources(usermod_modtcc INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}/modtcc.c
    ${CMAKE_CURRENT_LIST_DIR}/crypto/bignum.c 
    ${CMAKE_CURRENT_LIST_DIR}/crypto/ecdsa.c 
    ${CMAKE_CURRENT_LIST_DIR}/crypto/curves.c 
    ${CMAKE_CURRENT_LIST_DIR}/crypto/secp256k1.c 
    ${CMAKE_CURRENT_LIST_DIR}/crypto/nist256p1.c 
    ${CMAKE_CURRENT_LIST_DIR}/crypto/rand.c 
    # ${CMAKE_CURRENT_LIST_DIR}/crypto/hmac.c 
    ${CMAKE_CURRENT_LIST_DIR}/crypto/pbkdf2.c 
    ${CMAKE_CURRENT_LIST_DIR}/crypto/address.c 
    ${CMAKE_CURRENT_LIST_DIR}/crypto/script.c
    ${CMAKE_CURRENT_LIST_DIR}/crypto/ripemd160.c 
    ${CMAKE_CURRENT_LIST_DIR}/crypto/sha2.c 
    ${CMAKE_CURRENT_LIST_DIR}/crypto/sha3.c 
    ${CMAKE_CURRENT_LIST_DIR}/crypto/base58.c
    ${CMAKE_CURRENT_LIST_DIR}/crypto/blake256.c
    ${CMAKE_CURRENT_LIST_DIR}/crypto/hasher.c
    ${CMAKE_CURRENT_LIST_DIR}/crypto/ed25519-donna/curve25519-donna-32bit.c
    ${CMAKE_CURRENT_LIST_DIR}/crypto/ed25519-donna/curve25519-donna-helpers.c 
    ${CMAKE_CURRENT_LIST_DIR}/crypto/ed25519-donna/modm-donna-32bit.c 
    ${CMAKE_CURRENT_LIST_DIR}/crypto/ed25519-donna/ed25519-donna-basepoint-table.c 
    ${CMAKE_CURRENT_LIST_DIR}/crypto/ed25519-donna/ed25519-donna-32bit-tables.c 
    ${CMAKE_CURRENT_LIST_DIR}/crypto/ed25519-donna/ed25519-donna-impl-base.c 
    ${CMAKE_CURRENT_LIST_DIR}/crypto/ed25519-donna/ed25519.c 
    ${CMAKE_CURRENT_LIST_DIR}/crypto/ed25519-donna/curve25519-donna-scalarmult-base.c
)

# Add the current directory as an include directory.
target_include_directories(usermod_modtcc INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}
    ${CMAKE_CURRENT_LIST_DIR}/crypto

)
target_compile_definitions(usermod_modtcc INTERFACE
    MODULE_TREZORCRYPTO_ENABLED=1
    USE_BIP39_CACHE=0
    BIP32_CACHE_SIZE=0
    USE_BIP32_CACHE=0
    BIP32_CACHE_MAXDEPTH=0 
    USE_BIP39_GENERATE=0
    USE_BIP32_25519_CURVES=0
)
# Link our INTERFACE library to the usermod target.
target_link_libraries(usermod INTERFACE usermod_modtcc)
