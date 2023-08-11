import json
from web3 import Web3
import time
import random
import warnings
from conf import *

warnings.filterwarnings("ignore")  # Вытаскивая NFT_ID из хэша подлетает варнинг. Убираю его вывод.

# RPCs
polygon_rpc_url = 'https://polygon-rpc.com/'
w3 = Web3(Web3.HTTPProvider(polygon_rpc_url))
# ABI
abi = json.load(open('api.json'))
# NFT contract
contr_polygon_address = w3.to_checksum_address('0x141a1fb33683c304da7c3fe6fc6a49b5c0c2dc42')
nft_contract = w3.eth.contract(address=contr_polygon_address, abi=abi)

account = w3.eth.account.from_key(PRIVATE)
address = account.address

print(time.strftime("%H:%M:%S", time.localtime()))
print(f'{address}', flush=True)

def mint_poly(PRIVATE):
    try:
        swap_txn = nft_contract.functions.mint(
        ).build_transaction({
            'from': address,
            'maxFeePerGas': int(w3.eth.gas_price * 1.4),
            'maxPriorityFeePerGas': w3.eth.max_priority_fee,
            'nonce': w3.eth.get_transaction_count(address),
        })

        gasLimit = w3.eth.estimate_gas(swap_txn)
        swap_txn['gas'] = int(gasLimit * 1.4)  # Газ в матике сильно пляшет, врубаю сразу с большим запасом
        signed_swap_txn = w3.eth.account.sign_transaction(swap_txn, PRIVATE)
        swap_txn_hash = w3.eth.send_raw_transaction(signed_swap_txn.rawTransaction)

        # Check status of TX
        while True:
            try:
                if w3.eth.get_transaction_receipt(swap_txn_hash)['status'] != 1:
                    time.sleep(random.randint(10, 20))
                else:
                    time.sleep(random.randint(20, 50))
                    break
            except Exception as err:
                time.sleep(random.randint(20, 30))

        print(f"Transaction: https://polygonscan.com/tx/{swap_txn_hash.hex()}")

        tx_receipt = w3.eth.get_transaction_receipt(swap_txn_hash)
        transfer_event = nft_contract.events.Transfer()

        transfer_logs = transfer_event.process_receipt(tx_receipt)

        nft_id = transfer_logs[0]['args']['tokenId']

        with open(f'{address}_IDs.txt', 'a') as file:
            file.write(f'{nft_id}\n')  # храним сминченные NFT ID

    except Exception as err:
        print(f"Unexpected {err=}")


# Минтим НФТшки в полигоне
for i in range(6):
    mint_poly(PRIVATE)
    time.sleep(random.randint(20, 30))
