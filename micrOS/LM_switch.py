#########################################
#           DIGITAL IO SWITCH           #
#########################################
__SWITCH_OBJ = [None, None]
__PERSISTENT_CACHE = False
__SWITCH_STATE = [0, 0]

#########################################
#      SWITCH0 DIGITAL 0,1 OUTPUT       #
#########################################


def __SWITCH_init():
    if __SWITCH_OBJ[0] is None:
        from machine import Pin
        from LogicalPins import get_pin_on_platform_by_key
        __SWITCH_OBJ[0] = Pin(get_pin_on_platform_by_key('simple_0'), Pin.OUT)
    return __SWITCH_OBJ[0]


def __persistent_cache_manager(mode):
    """
    pds - persistent data structure
    modes:
        r - recover, s - save
    """
    if not __PERSISTENT_CACHE:
        return
    global __SWITCH_STATE
    if mode == 's':
        # SAVE CACHE
        with open('switch.pds', 'w') as f:
            f.write(','.join([str(k) for k in __SWITCH_STATE]))
        return
    try:
        # RESTORE CACHE
        with open('switch.pds', 'r') as f:
            __SWITCH_STATE = [int(data) for data in f.read().strip().split(',')]
    except:
        pass


def switch_cache_load_n_init(cache=None):
    from sys import platform
    global __PERSISTENT_CACHE
    if cache is None:
        __PERSISTENT_CACHE = True if platform == 'esp32' else False
    else:
        __PERSISTENT_CACHE = cache
    __persistent_cache_manager('r')
    if __PERSISTENT_CACHE and __SWITCH_STATE[0] == 1:
        set_state()
    else:
        set_state(0)
    return "CACHE: {}".format(__PERSISTENT_CACHE)


def set_state(state=None):
    state = __SWITCH_STATE[0] if state is None else state
    if state in (0, 1):
        __SWITCH_init().value(state)
        __SWITCH_STATE[0] = state
        __persistent_cache_manager('s')
    else:
        return "[ERROR] switch input have to 0 or 1"
    return "SET STATE: {}".format(state)


def toggle():
    """
    Toggle led state based on the stored one
    """
    new_state = 1 if __SWITCH_STATE[0] == 0 else 0
    return set_state(new_state)


#########################################
#      SWITCH1 DIGITAL 0,1 OUTPUT       #
#########################################


def __SWITCH2_init():
    if __SWITCH_OBJ[1] is None:
        from machine import Pin
        from LogicalPins import get_pin_on_platform_by_key
        __SWITCH_OBJ[1] = Pin(get_pin_on_platform_by_key('pwm_1'), Pin.OUT)
    return __SWITCH_OBJ[1]


def switch2_cache_load_n_init(cache=None):
    from sys import platform
    global __PERSISTENT_CACHE
    if cache is None:
        __PERSISTENT_CACHE = True if platform == 'esp32' else False
    else:
        __PERSISTENT_CACHE = cache
    __persistent_cache_manager('r')
    if __PERSISTENT_CACHE and __SWITCH_STATE[0] == 1:
        set_state2()
    else:
        set_state2(0)
    return "CACHE: {}".format(__PERSISTENT_CACHE)


def set_state2(state=None):
    state = __SWITCH_STATE[1] if state is None else state
    if state in (0, 1):
        __SWITCH2_init().value(state)
        __SWITCH_STATE[1] = state
        __persistent_cache_manager('s')
    else:
        return "[ERROR] switch input have to 0 or 1"
    return "SET STATE: {}".format(state)


def toggle2():
    """
    Toggle led state based on the stored one
    """
    new_state = 1 if __SWITCH_STATE[1] == 0 else 0
    return set_state2(new_state)


#########################################
#                   HELP                #
#########################################

def help():
    return 'set_state state=<0,1>', 'toggle',\
           'switch_cache_load_n_init cache=None<True/False>',\
           'set_state2 state=<0,1>', 'toggle2',\
           'switch2_cache_load_n_init cache=None<True/False>',\
           '[!]PersistentStateCacheDisabledOn:esp8266'
