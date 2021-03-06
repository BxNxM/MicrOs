from sys import platform
#########################################
#       DIGITAL CONTROLLER PARAMS       #
#########################################
# Values: R, G, B, STATE_ON_OFF, IS_INITIALIZED
__DCACHE = [100, 100, 100, 0]
__NEOPIXEL_OBJ = None
__PERSISTENT_CACHE = False


#########################################
#        DIGITAL rgb WITH 1 "PWM"       #
#########################################


def __init_NEOPIXEL(n=24):
    """
    Init NeoPixel module
    n - number of led fragments
    n - must be set from code! (no persistent object handling in LMs)
    """
    global __NEOPIXEL_OBJ
    if __NEOPIXEL_OBJ is None:
        from neopixel import NeoPixel
        from machine import Pin
        from LogicalPins import get_pin_on_platform_by_key
        neopixel_pin = Pin(get_pin_on_platform_by_key('pwm_3'))     # Get Neopixel pin from LED PIN pool
        __NEOPIXEL_OBJ = NeoPixel(neopixel_pin, n)                  # initialize for max 8 segments
        del neopixel_pin
    return __NEOPIXEL_OBJ


def __persistent_cache_manager(mode):
    """
    pds - persistent data structure
    modes:
        r - recover, s - save
    """
    if not __PERSISTENT_CACHE:
        return
    global __DCACHE
    if mode == 's':
        # SAVE CACHE
        with open('neopixel.pds', 'w') as f:
            f.write(','.join([str(k) for k in __DCACHE]))
        return
    try:
        # RESTORE CACHE
        with open('neopixel.pds', 'r') as f:
            __DCACHE = [int(data) for data in f.read().strip().split(',')]
    except:
        pass


def neopixel_cache_load_n_init(cache=None):
    global __PERSISTENT_CACHE
    if cache is None:
        __PERSISTENT_CACHE = False if platform == 'esp8266' else True
    else:
        __PERSISTENT_CACHE = cache
    __persistent_cache_manager('r')        # recover data cache
    if __PERSISTENT_CACHE and __DCACHE[3] == 1:
        neopixel()                         # Set each LED for the same color
    return "CACHE: {}".format(__PERSISTENT_CACHE)


def neopixel(r=None, g=None, b=None):
    """
    Simple NeoPixel wrapper
    - Set all led fragments for the same color set
    - Default and cached color scheme
    """
    global __DCACHE
    r = __DCACHE[0] if r is None else r
    g = __DCACHE[1] if g is None else g
    b = __DCACHE[2] if b is None else b
    # Set each LED for the same color
    for element in range(0, __init_NEOPIXEL().n):    # Iterate over led string elements
        __NEOPIXEL_OBJ[element] = (r, g, b)             # Set LED element color
    __NEOPIXEL_OBJ.write()                              # Send data to device
    # Set cache
    if r > 0 or g > 0 or b > 0:
        __DCACHE = [r, g, b, 1]                         # Cache colors + state (True-ON)
    else:
        __DCACHE[3] = 0                                 # State - False - OFF
    __persistent_cache_manager('s')                # Save cache - __DCACHE -  to file
    return "NEOPIXEL SET TO R{}G{}B{}".format(r, g, b)


def segment(r=None, g=None, b=None, s=0):
    r = __DCACHE[0] if r is None else r
    g = __DCACHE[1] if g is None else g
    b = __DCACHE[2] if b is None else b
    if s <= __init_NEOPIXEL().n:
        __NEOPIXEL_OBJ[s] = (r, g, b)
        __NEOPIXEL_OBJ.write()
        return "NEOPIXEL {} SEGMENT WAS SET R{}G{}B{}".format(s, r, g, b)
    return "NEOPIXEL s={} SEGMENT OVERLOAD".format(s)


def toggle(state=None):
    """
    ON - OFF NeoPixel
    """
    if state is not None:
        __DCACHE[3] = 0 if state else 1
    if __DCACHE[3] == 1:
        neopixel(r=0, g=0, b=0)
        return "OFF"
    neopixel(__DCACHE[0], __DCACHE[1], __DCACHE[2])
    return "ON"

#########################################
#                   HELP                #
#########################################


def help():
    return 'neopixel(r=<0-255>, g, b, n=24', 'toggle(state=None)', \
           'neopixel_cache_load_n_init(cache=None<True/False>', \
           'segment(r, g, b, s=<0-n>', '[!]PersistentStateCacheDisabledOn:esp8266'
