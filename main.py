"""
# TODO docs
"""
# importing standard library modules
import os, sys, json
from time import sleep

import errors
import tools
import p2sh

try:
    from bitcoinutils.setup import setup
except ModuleNotFoundError as e:
        errors.environment(e)

if __name__ == '__main__':
    try:  # get script argument (mode)
        mode = sys.argv[1]
    except:
        errors.missing_mode()

    # ensure that bitcoind is running
    r1 = os.system('bitcoin-cli ping')
    if r1 != 0:
        print('Starting bitcoin client')
        r2 = os.system('bitcoind -daemon')
        if r2 != 0:
            print('Error: Unable to start bitcoind, pls manually start/install\n')
            raise SystemExit
        print('Waiting for blocks to rewind...\n')
        while True:
            r3 = os.system('bitcoin-cli ping')
            if r3 == 0:
                break
            sleep(1)

    # run function of mode
    run = {'config_data': tools.config_data,
           'p2sh_create': p2sh.csv_script,
           'p2sh_fill': p2sh.fill, 
           'p2sh_spend': p2sh.spend_all}
    if mode in run:
        setup('testnet')
        run[mode]()
    else:
        errors.missing_mode()  # prints error msg & raises SsstemExit
