import json
from web3 import Web3
import time
import random
from conf import *

# RPCs

w3 = Web3(Web3.HTTPProvider('https://endpoints.omniatech.io/v1/bsc/testnet/public'))
# ABI
abi_bridge_bnb = json.load(open('abi_bridge_bnb.json'))

bridge_address = w3.to_checksum_address('0x677311fd2ccc511bbc0f581e8d9a07b033d5e840')
bridge_contract = w3.eth.contract(address=bridge_address, abi=abi_bridge_bnb)

bridge_address2 = w3.to_checksum_address('0x261436b25a95449350c1eb11882f46f4140dbf74') # combonetwork
bridge_contract2 = w3.eth.contract(address=bridge_address2, abi=abi_bridge_bnb)

account = w3.eth.account.from_key(PRIVATE)
address = account.address

print(time.strftime("%H:%M:%S", time.localtime()))
print(f'{address}', flush=True)

bnb_balance = w3.eth.get_balance(address)
half_of_balance = int((bnb_balance / 2) * 0.7)


print(bnb_balance)

def bnb_br(bridge_contract, value):
    _l2Gas = 200000
    b = b''
    try:
        swap_txn = bridge_contract.functions.depositETH(_l2Gas, b
                                                        ).build_transaction({
            'from': address,
            'value': value,
            'gasPrice': w3.eth.gas_price,
            'chainId': 97,
            'nonce': w3.eth.get_transaction_count(address),
        })
        gasLimit = w3.eth.estimate_gas(swap_txn)
        swap_txn['gas'] = int(gasLimit * 1.4)
        signed_swap_txn = w3.eth.account.sign_transaction(swap_txn, PRIVATE)
        swap_txn_hash = w3.eth.send_raw_transaction(signed_swap_txn.rawTransaction)
        print(f"Transaction: https://testnet.bscscan.com/tx/{swap_txn_hash.hex()}")

    except Exception as err:
        print(f"Unexpected {err=}")


bnb_br(bridge_contract, half_of_balance)
time.sleep(30)
bnb_br(bridge_contract2, half_of_balance)

#https://opbnbscan.com/address/
