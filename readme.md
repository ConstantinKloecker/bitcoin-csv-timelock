# Bitcoin : P2SH Address with Relative Timelock Script

This program is able to generate a P2SH address with a CSV timelock, as well as 
spending all UTXOs associated with the P2SH address. Both these functions can be accomplished by following the instructions below.

When sending funds to the P2SH address, the UTXOs will be locked until they have 
been confirmed for the specified amount of blocks. Additionally, the program 
assumes that the bitcoin core client is installed locally!

**!!! Be aware, this program is purely intended for educational purposes, and 
should only be used on the Bitcoin testnet !!!**


-----
## 1. Setting up project environment

#### 1.1 Run setup.py for automated setup:
    
    $ python3 setup.py
- creates new venv
- installs dependencies
- confirms succesfull setup

#### 1.2 Alternatively, setup environment manually:  
    
    $ mkdir venv
    $ python3 -m venv venv
    $ source ./venv/bin/activate
    $ pip3 install bitcoin-utils requests


-----
## 2. Configure data.json

#### 2.1 keys: pub_key (hex) or priv_key (wif)
- eg. pub_key: "023e17859419f46552bc0a5856ff8f7f523b7e877ec8bde3fd53334a5b13a14fae"
- eg. priv_key: "cUD74njAVhJAsCV1Npg9zY2fCPFTFe6pfJ6nPAEweBMBjP9ZenZs"

If both keys are provided, the program defaults to using priv_key. The priv_key 
must be included in order to spend from the P2SH address.

#### 2.2 timelock: block_height (int)
  - eg. block_height: 200

#### 2.3 p2pkh_address: for spending script
  - eg. p2pkh_address: "mttbFoMwL3g4Y3UTfMin19hx2x9i94nE7D"


-----
## 3. Create a new P2SH address
 
    $ source ./venv/bin/activate
    $ python3 main.py create_p2sh
- creates a new P2SH address with csv script
- adddress & script hash is displayed in terminal and saved in data.json

Now manually send BTC to the P2SH address. Wait for thr UTXOs to be confirmed 
enough times until they satify they timelock (block height) condition.


-----
## 4. Spend from P2SH address

    $ source ./venv/bin/activate
    $ python3 main.py spend_p2sh
- creates a transaction that spends all UTXOs of P2SH address,
- broadcasts the transaction via bitcoin-cli
- tx_id & tx_signed is displayed in terminal and saved in data.json

Note: The program assumes that the UTXOs send to the P2SH address were created/signed/broadcasted from the locally running bitcoin client, this 
assumption is critical for the program to automatically gather the input UTXOs 
for creating the spending from P2SH address transaction. If this assumption does 
not hold, then the program is unable to collect the transaction input UTXOs for 
the spending transaction. The program is able to handle multiple UTXOs send to 
the P2SH address.

Additionally, the program estimates the required fee for sending the transaction, 
if the required fee is larger than the balance of the P2SH's UTXOs, then the 
program will prompt the user to either exit and send additional balance to the 
P2SH address, or to specify a custom fee.


-----
## 5. Additional Resources to learn about Bitcoin Scripts

- https://github.com/ChristopherA/Learning-Bitcoin-from-the-Command-Line

- https://github.com/karask/python-bitcoin-utils/tree/master/examples
