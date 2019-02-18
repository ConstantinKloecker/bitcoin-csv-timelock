"""
P2SH functions
--------------
    - csv_script
    - fill
    - spend_all
"""

import json
import requests

import errors
import tools

from bitcoinutils.script import Script
from bitcoinutils.keys import P2shAddress
from bitcoinutils.transactions import Transaction, TxInput, TxOutput


def csv_script(recreate=False):
    """ creates a P2SH address with a relative csv timelock script
    
    Attributes
    ----------
    recreate : boolean
        False (default) -> used when creating new p2sh addr (save and display)
        True -> used when spending from p2sh address (returns objects for TX)
    
    returns
    -------
    if recreate=False (default - used when creating new p2sh addres)
        returns nothing
        - writes p2sh address into data.json
        - displays p2sh address to the user
    if recreate=True (used to recreate script when spending form p2sh address)
        returns csv_script (Script Object), p2sh_addr (P2shAddress Object)
    """
    # load csv script data (pub_key_hash, timelock_period) from data.json
    data = tools.load_data_json(pub_hash=True, timelock_csv=True, 
        timelock_log=True)
    pub_key_hash = data['pub_key_hash']
    timelock_period = data['timelock_csv']
    timelock_str = data['timelock_log']

    # initiate script object
    csv_script = Script([timelock_period, 'OP_CHECKSEQUENCEVERIFY', 'OP_DROP',
        'OP_DUP', 'OP_HASH160', pub_key_hash, 'OP_EQUALVERIFY', 'OP_CHECKSIG'])
    # get P2SH address of csv_script
    p2sh_addr = P2shAddress.from_script(csv_script).to_address()
    csv_hash = csv_script.to_hex()

    if recreate:  # used when spending from p2sh
       return csv_script, p2sh_addr
    
    # used when creating initial p2sh
    # - writes p2sh address into data.json
    # - displays p2sh address (+details) to the user via terminal
    tools.update_data_json(outputs={'p2sh_address': p2sh_addr, 'csv_hash': csv_hash})
    print('\nNew p2sh address with CSV script created')
    print(' -> timelock period for:', timelock_str, 'blocks')
    print(' -> script_hash:', csv_hash)
    print(' -> p2sh_addr:', p2sh_addr, '\n')


def fill():
    """ send 1/10th of the cli's balance to the P2SH"""
    _, p2sh_address = csv_script(recreate=True)
    cli_balance = float(tools.talk_to_cli('bitcoin-cli getbalance', True))
    amount = round(cli_balance/10, 8)
    tools.talk_to_cli(f'bitcoin-cli sendtoaddress {p2sh_address} {amount}')
    print(f'\n {cli_balance/10} BTC send to P2SH address ({p2sh_address})\n')


def spend_all():
    """ creates & broadcasts a transactions that spend all UTXOs from the P2SH"""
    # loads script data (Script, p2sh_addr)
    script, p2sh_addr = csv_script(recreate=True)

    # load transaction data(PrivateKey, timelock, P2pkhAddresses) from data.json
    data = tools.load_data_json(priv=True, timelock_tx=True, p2pk=True)
    priv_key = data['priv_key']
    tx_lock = data['timelock_tx'] 
    p2pkh_addr = data['p2pk_addr']

    # query cli to detect transactions send to the p2sh adddress
    # gathers txid, vout, and amount of p2sh's UTXOs to create TxInputs
    p2sh_utxos, p2sh_balance = [], 0
    wallet_txs = tools.talk_to_cli('bitcoin-cli listtransactions * 900', True)
    for tx in json.loads(wallet_txs):
        if tx['address'] == p2sh_addr and tx['category'] == 'send':
            p2sh_utxos.append(TxInput(tx['txid'], tx['vout'], sequence=tx_lock))
            p2sh_balance += (-tx['amount'])
    # confirm that bitcoin-cli was able to locate transactions to p2sh address
    if not p2sh_utxos:
        errors.missing_utxos()  # prints error msg & raises systemExit

    # check current network fees and compute fee estimate
    resp = requests.get('https://api.blockcypher.com/v1/btc/test3').json()
    fee_per_kb = resp['medium_fee_per_kb']
    # per Output: 34 bytes | per Input: 200 bytes (estimate)
    script_size = 1 * 34 + len(p2sh_utxos) * 200
    fee = (script_size * fee_per_kb) / 100000000
    if fee >= p2sh_balance:
        fee = tools.user_custom_fee(fee, p2sh_balance)        

    # create and sign transaction
    tx_out = TxOutput((p2sh_balance-fee), p2pkh_addr.to_script_pub_key())
    # no change address, spending entire balance
    tx = Transaction(p2sh_utxos, [tx_out])
    pub_key = priv_key.get_public_key().to_hex()
    for i, txin in enumerate(p2sh_utxos):
        sig = priv_key.sign_input(tx, i, script)
        txin.script_sig = Script([sig, pub_key, script.to_hex()])
    tx_signed, tx_id = tx.serialize(), tx.get_txid()

    # writes tx_id into data.json and displays tx_signed (+details) to the user
    tools.update_data_json(outputs={'tx_id': tx_id, 'tx_signed': tx_signed})
    print('\nSpending from P2SH transaction')
    print(' -> to_addr:', p2pkh_addr.to_address())
    print(' -> amount:', p2sh_balance-fee)
    print(' -> fee:', fee)
    print(' -> tx_id:', tx_id)
    print(' -> tx_signed:',tx_signed, '\n')

    # broadcast signed transaction over bitcoin-cli
    r = tools.talk_to_cli(f'bitcoin-cli sendrawtransaction {tx_signed}', True)
    if len(r) == 64:
        print('\nTransaction broadcasted via bitcoin-cli successfully\n')
