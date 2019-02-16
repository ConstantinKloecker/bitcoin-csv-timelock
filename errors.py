"""
errors
------
    - environment
    - missing_data
    - estimated_fee_2_large
    - custom_fee_2_large
    - missing_utxos
    - missing_mode
"""

def environment(exception):
    print('\n', exception, '\n')
    print('\nError: project venv not activated!')
    print('Please setup & activate venv as follows:')
    print(' - setup:    $ python3 setup.py')
    print(' - activate: $ source ./venv/bin/activate\n')
    raise SystemExit

def missing_data(component):
    """helper function called when data.json is not configured fully"""
    print(f'\nError: user {component} not configured!')
    print(f'Please configure {component} in data.json\n')
    raise SystemExit

def estimated_fee_2_large(fee, p2sh_balance):
    print('\nError: estimated fee larger than P2SH balance!')
    print(f'Estimated fee: {fee}  |  Balance: {p2sh_balance}')
    print('Please add balance to P2SH address or set a custom fee\n')

def custom_fee_2_large(c_fee, p2sh_balance):
    print('\nError: custom fee larger than balance!')
    print(f'Custom fee: {c_fee}  |  Balance: {p2sh_balance}\n')

def missing_utxos():
    print('\nError: local bitcoin-cli has no record of p2sh inputs!')
    print('It appears that the transactions to the p2sh address have been')
    print('created from a different bitcoin client. Please send some BTC')
    print('to the p2sh address from the local bitcoin-cli client\n')
    raise SystemExit

def missing_mode():
    print('\nError: No valid mode specified!')
    print('Please specify mode as follows:')
    print('-------------------------------')
    print('- To automatically configure data.json:')
    print('  $ python3 main.py config_data\n')
    print('- To create a p2sh address:')
    print('  $ python3 main.py p2sh_create\n')
    print('- To fill the p2sh address with BTC:')
    print('  $ python3 main.py p2sh_fill\n')
    print('- To spend from the p2sh address:')
    print('  $ python3 main.py p2sh_spend\n')
    raise SystemExit
