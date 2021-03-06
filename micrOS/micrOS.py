"""
Module is responsible for high level function invocations
dedicated to micrOS framework.

Designed by Marcell Ban aka BxNxM
"""
#################################################################
#                           IMPORTS                             #
#################################################################
from Network import auto_network_configuration
from SocketServer import SocketServer
from Hooks import bootup_hook, profiling_info

#################################################################
#            INTERRUPT HANDLER INTERFACES / WRAPPERS            #
#################################################################


def safe_boot_hook():
    try:
        bootup_hook()
    except Exception as e:
        print("[micrOS main] Hooks.bootup_hook() error: {}".format(e))


def interrupt_handler():
    try:
        from InterruptHandler import enableInterrupt
        enableInterrupt()
    except Exception as e:
        print("[micrOS main] InterruptHandler.enableInterrupt error: {}".format(e))


def external_interrupt_handler():
    try:
        from InterruptHandler import init_eventPIN
        init_eventPIN()
    except Exception as e:
        print("[micrOS main] InterruptHandler.init_eventPIN error: {}".format(e))


#################################################################
#                      MAIN FUNCTION CALLS                      #
#################################################################

def micrOS():
    profiling_info(label='[1] MAIN BASELOAD')

    # BOOT HOOKs execution
    safe_boot_hook()
    profiling_info(label='[2] AFTER SAFE BOOT HOOK')

    # NETWORK setup
    auto_network_configuration()
    profiling_info(label='[3] AFTER NETWORK CONFIGURATION')

    # LOAD Singleton SocketServer [1]
    SocketServer()
    profiling_info(label='[4] AFTER SOCKET SERVER CREATION')

    # SET interrupt with timirqcbf from nodeconfig
    interrupt_handler()
    profiling_info(label='[5] AFTER TIMER INTERRUPT SETUP')

    # SET external interrupt with extirqcbf from nodeconfig
    external_interrupt_handler()
    profiling_info(label='[6] AFTER EXTERNAL INTERRUPT SETUP')

    # RUN Singleton SocketServer - main loop [2]
    SocketServer().run()

