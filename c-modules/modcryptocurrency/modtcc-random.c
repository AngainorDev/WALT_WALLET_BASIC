/*
 * Copyright (c) Pavol Rusnak, SatoshiLabs
 *
 * Licensed under TREZOR License
 * see LICENSE file for details
 */

#include "py/objstr.h"

#include "rand.h"

/// def uniform(n: int) -> int:
///     '''
///     Compute uniform random number from interval 0 ... n - 1.
///     '''
STATIC mp_obj_t mod_trezorcrypto_random_uniform(mp_obj_t n) {
    uint32_t nn = mp_obj_int_get_checked(n);
    if (nn == 0) {
        mp_raise_ValueError(MP_ERROR_TEXT("Maximum can't be zero"));
    }
    return mp_obj_new_int_from_uint(random_uniform(nn));
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(mod_trezorcrypto_random_uniform_obj, mod_trezorcrypto_random_uniform);

/// def bytes(len: int) -> bytes:
///     '''
///     Generate random bytes sequence of length len.
///     '''
STATIC mp_obj_t mod_trezorcrypto_random_bytes(mp_obj_t len) {
    uint32_t l = mp_obj_get_int(len);
    if (l > 1024) {
        mp_raise_ValueError(MP_ERROR_TEXT("Maximum requested size is 1024"));
    }
    vstr_t vstr;
    vstr_init_len(&vstr, l);
    random_buffer((uint8_t *)vstr.buf, l);
    return mp_obj_new_str_from_vstr(&mp_type_bytes, &vstr);
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(mod_trezorcrypto_random_bytes_obj, mod_trezorcrypto_random_bytes);

/// def shuffle(data: list) -> None:
///     '''
///     Shuffles items of given list (in-place).
///     '''
STATIC mp_obj_t mod_trezorcrypto_random_shuffle(mp_obj_t data) {
    size_t count;
    mp_obj_t *items;
    mp_obj_get_array(data, &count, &items);
    if (count > 256) {
        mp_raise_ValueError(MP_ERROR_TEXT("Maximum list size is 256 items"));
    }
    if (count <= 1) {
        return mp_const_none;
    }
    // Fisher-Yates shuffle
    mp_obj_t t;
    for (size_t i = count - 1; i >= 1; i--) {
        size_t j = random_uniform(i + 1);
        t = items[i];
        items[i] = items[j];
        items[j] = t;
    }
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(mod_trezorcrypto_random_shuffle_obj, mod_trezorcrypto_random_shuffle);

STATIC const mp_rom_map_elem_t mod_trezorcrypto_random_globals_table[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_random) },
    { MP_ROM_QSTR(MP_QSTR_uniform), MP_ROM_PTR(&mod_trezorcrypto_random_uniform_obj) },
    { MP_ROM_QSTR(MP_QSTR_bytes), MP_ROM_PTR(&mod_trezorcrypto_random_bytes_obj) },
    { MP_ROM_QSTR(MP_QSTR_shuffle), MP_ROM_PTR(&mod_trezorcrypto_random_shuffle_obj) },
};
STATIC MP_DEFINE_CONST_DICT(mod_trezorcrypto_random_globals, mod_trezorcrypto_random_globals_table);

STATIC const mp_obj_module_t mod_trezorcrypto_random_module = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t*)&mod_trezorcrypto_random_globals,
};
