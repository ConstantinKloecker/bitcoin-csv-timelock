import os

if __name__ == '__main__':
    print('\nSetting up project environment ...')

    # setting up venv
    print('Building new virtual environment ...')
    os.system('mkdir venv')
    r0 = os.system('python3 -m venv venv')
    if r0 != 0:
        print('\n !!! Error while buidling venv, please setup manually\n')
        raise SystemExit
    activate_venv = '. ./venv/bin/activate'

    # installing modules
    print('Installing dependencies ...\n')
    os.system(f'{activate_venv} && pip3 install requests')
    os.system(f'{activate_venv} && pip3 install git+git://github.com/karask/python-bitcoin-utils')

    # testing project environment
    print('\n\nTesting project environment:')
    print('----------------------------')
    print(' - venv available')
    # verifying that bitcoinutils is available
    e1, e2 = None, None
    r1 = os.system(f"{activate_venv} && python3 -c 'import bitcoinutils'")
    if r1 == 0:
        print(' - bitcoin-utils available')
    else:
        print('\n  !!! Error while importing bitcoinutils\n')
        e1 = True
    # verifying that requests is available
    r2 = os.system(f"{activate_venv} && python3 -c 'import requests'")
    if r2 == 0:
        print(' - requests available')
    else:
        print('\n  !!! Error while importing requests\n')
        e2 = True
    # communicating result to the user
    if e1 or e2:
        print('\n  !!! Problem during setup, please setup project manually\n')
    else:
        print('----------------------------')
        print('\nProject environment setup complete. You are ready to go!')
        print(' - configure data.json with relevant user inputs.')
        print(' - activate venv: $ source ./venv/bin/activate\n')
        print('Finally, run the program as follows:')
        print('------------------------------------')
        print('- To create a p2sh address:')
        print('  $ python3 main.py create_p2sh\n')
        print('- To spend from p2sh address:')
        print('  $ python3 main.py spend_p2sh\n')
