# this is our module path
USERMODULE_DIR := $(USERMOD_DIR)

# Add all C files to SRC_USERMOD.
SRC_USERMOD += $(USERMODULE_DIR)/modtcc.c

CFLAGS_USERMOD += -I$(USERMODULE_DIR)
#CFLAGS_USERMOD += -I/media/sylvain/d41898c7-b02c-4c9d-9234-142b764e3336/git/micropython-pca10059/ports/nrf/boards/pca10059/crypto

CFLAGS_USERMOD += -Icrypto
# CFLAGS_USERMOD += -Wno-unused-variable

#SRC_USERMOD += $(addprefix boards/$(BOARD)/crypto/,\
#				bignum.c ecdsa.c curves.c secp256k1.c nist256p1.c \
#				rand.c hmac.c pbkdf2.c \
#				bip32.c bip39.c base58.c base32.c segwit_addr.c \
#				address.c script.c \
#				ripemd160.c sha2.c sha3.c hasher.c \
#				blake256.c blake2b.c blake2s.c \
#				aes/aescrypt.c aes/aeskey.c aes/aestab.c aes/aes_modes.c \
#				ed25519-donna/curve25519-donna-32bit.c \
#				ed25519-donna/curve25519-donna-helpers.c \
#				ed25519-donna/modm-donna-32bit.c \
#				ed25519-donna/ed25519-donna-basepoint-table.c \
#				ed25519-donna/ed25519-donna-32bit-tables.c \
#				ed25519-donna/ed25519-donna-impl-base.c \
#				ed25519-donna/ed25519.c \
#				ed25519-donna/curve25519-donna-scalarmult-base.c \
#				ed25519-donna/ed25519-keccak.c \
#				ed25519-donna/ed25519-sha3.c \
#				chacha20poly1305/chacha20poly1305.c \
#				chacha20poly1305/chacha_merged.c \
#				chacha20poly1305/poly1305-donna.c \
#				chacha20poly1305/rfc7539.c \
#				)

				
SRC_USERMOD += $(addprefix crypto/,\
				bignum.c ecdsa.c curves.c secp256k1.c nist256p1.c \
				rand.c hmac.c pbkdf2.c \
				address.c script.c \
				ripemd160.c sha2.c sha3.c hasher.c \
				ed25519-donna/curve25519-donna-32bit.c \
				ed25519-donna/curve25519-donna-helpers.c \
				ed25519-donna/modm-donna-32bit.c \
				ed25519-donna/ed25519-donna-basepoint-table.c \
				ed25519-donna/ed25519-donna-32bit-tables.c \
				ed25519-donna/ed25519-donna-impl-base.c \
				ed25519-donna/ed25519.c \
				ed25519-donna/curve25519-donna-scalarmult-base.c )


# settings that apply only to crypto C-lang code
build-pca10059-s140/boards/pca10059/crypto/%.o: CFLAGS_MOD += \
	-DUSE_BIP39_CACHE=0 -DBIP32_CACHE_SIZE=0 -DUSE_BIP32_CACHE=0 -DBIP32_CACHE_MAXDEPTH=0 \
	-DUSE_BIP39_GENERATE=0 -DUSE_BIP32_25519_CURVES=0
	
# -DRAND_PLATFORM_INDEPENDENT=1 
