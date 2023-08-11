import json
from web3 import Web3
import time
import random
from conf import *

# RPCs
polygon_rpc_url = 'https://polygon-rpc.com/'
w3 = Web3(Web3.HTTPProvider(polygon_rpc_url))
# ABI
abi = json.load(open('api.json'))
abi_bridge = json.load(open('abi_bridge.json'))
lz_abi_bridge = json.load(open('lz_abi_bridge.json'))

# NFT contract
contr_polygon_address = w3.to_checksum_address('0x141a1fb33683c304da7c3fe6fc6a49b5c0c2dc42')
bridge_address = w3.to_checksum_address('0x2e953a70c37e8cb4553dae1f5760128237c8820d')
nft_contract = w3.eth.contract(address=contr_polygon_address, abi=abi)
bridge_contract = w3.eth.contract(address=bridge_address, abi=abi_bridge)
lz_bridge_address = w3.to_checksum_address('0xffdf4fe05899c4bdb1676e958fa9f21c19ecb9d5')
lz_bridge_contract = w3.eth.contract(address=lz_bridge_address, abi=lz_abi_bridge)

account = w3.eth.account.from_key(PRIVATE)
address = account.address

print(time.strftime("%H:%M:%S", time.localtime()))
print(f'{address}', flush=True)


def approve(contr_bridge, nft_id):
    nonce = w3.eth.get_transaction_count(address)

    to = w3.to_checksum_address(contr_bridge)

    try:
        approve_txn = nft_contract.functions.approve(to,
                                                     nft_id).build_transaction({
            'from': address,
            'maxFeePerGas': int(w3.eth.gas_price * 1.4),
            'maxPriorityFeePerGas': w3.eth.max_priority_fee,
            'nonce': nonce,
        })

        gasLimit = w3.eth.estimate_gas(approve_txn)
        approve_txn['gas'] = int(gasLimit * 1.4)  # Газ в матике сильно пляшет, врубаю сразу с большим запасом
        signed_approve_txn = w3.eth.account.sign_transaction(approve_txn, PRIVATE)
        approve_txn_hash = w3.eth.send_raw_transaction(signed_approve_txn.rawTransaction)
        # Проверяем транзу
        while True:
            try:
                if w3.eth.get_transaction_receipt(approve_txn_hash)['status'] != 1:
                    time.sleep(random.randint(10, 20))
                    print('status:', w3.eth.get_transaction_receipt(approve_txn_hash)['status'])
                else:
                    print(f"NFT APPROVED https://polygonscan.com/tx/{approve_txn_hash.hex()}")
                    time.sleep(random.randint(20, 50))
                    break
            except Exception as err:
                time.sleep(random.randint(20, 30))

        return True

    except Exception as err:
        print(f"Unexpected {err=}")
        return False


# Отправка нфт в первую залупу

def bridge_nft(tokenID, recipientChain):
    nonce = w3.eth.get_transaction_count(address)

    token = contr_polygon_address

    recipient = '0x000000000000000000000000' + address[2:]

    fee = bridge_contract.functions.fee(recipientChain).call()

    try:
        bridge_txn = bridge_contract.functions.transferNFT(token,
                                                           tokenID, recipientChain, recipient).build_transaction({
            'from': address,
            'value': fee,
            'maxFeePerGas': int(w3.eth.gas_price * 1.4),
            'maxPriorityFeePerGas': w3.eth.max_priority_fee,
            'nonce': nonce,
        })

        gasLimit = w3.eth.estimate_gas(bridge_txn)
        bridge_txn['gas'] = int(gasLimit * 1.4)
        signed_bridge_txn = w3.eth.account.sign_transaction(bridge_txn, PRIVATE)
        bridge_txn_hash = w3.eth.send_raw_transaction(signed_bridge_txn.rawTransaction)
        # Проверяем транзу
        while True:
            try:
                if w3.eth.get_transaction_receipt(bridge_txn_hash)['status'] != 1:
                    time.sleep(random.randint(20, 30))

                else:
                    time.sleep(random.randint(20, 50))
                    break
            except Exception as err:
                time.sleep(random.randint(20, 30))

        print(f"NFT Bridged https://polygonscan.com/tx/{bridge_txn_hash.hex()}")

        with open(f'{address}_hashes.txt', 'a') as file:
            file.write(f'{bridge_txn_hash.hex()}\n')  # храним хэши, от не L0 бриджей нфт

    except Exception as err:
        print(f"Unexpected {err=}")
        return False


def lz_bridge_nft(tokenID, recipientChain):
    nonce = w3.eth.get_transaction_count(address)

    token = contr_polygon_address
    recipient = address
    _adapterParams = '0x00010000000000000000000000000000000000000000000000000000000000055730'
    fee = lz_bridge_contract.functions.estimateFee(token, tokenID, recipientChain, recipient,
                                                   _adapterParams).call()

    try:
        bridge_txn = lz_bridge_contract.functions.transferNFT(token,
                                                              tokenID, recipientChain, recipient,
                                                              _adapterParams).build_transaction({
            'from': address,
            'value': fee,
            'maxFeePerGas': int(w3.eth.gas_price * 1.4),
            'maxPriorityFeePerGas': w3.eth.max_priority_fee,
            'nonce': nonce,
        })

        gasLimit = w3.eth.estimate_gas(bridge_txn)
        bridge_txn['gas'] = int(gasLimit * 1.4)
        signed_bridge_txn = w3.eth.account.sign_transaction(bridge_txn, PRIVATE)
        bridge_txn_hash = w3.eth.send_raw_transaction(signed_bridge_txn.rawTransaction)
        # Проверяем транзу
        while True:
            try:
                if w3.eth.get_transaction_receipt(bridge_txn_hash)['status'] != 1:
                    time.sleep(random.randint(20, 30))

                else:
                    time.sleep(random.randint(20, 50))
                    break
            except Exception as err:
                time.sleep(random.randint(20, 30))

        print(f"NFT Bridged https://polygonscan.com/tx/{bridge_txn_hash.hex()}")

    except Exception as err:
        print(f"Unexpected {err=}")
        return False


with open(f'{address}_IDs.txt', 'r') as nft:
    nft1 = int(nft.readline())
    nft2 = int(nft.readline())
    nft3 = int(nft.readline())
    nft4 = int(nft.readline())
    nft5 = int(nft.readline())
    nft6 = int(nft.readline())

# Начинаем аппрувы и бриджи НФТ

approve('0x2E953a70C37E8CB4553DAe1F5760128237c8820D', nft1)
time.sleep(40)
bridge_nft(nft1, 116)  # Отправляем первую НФТ в opBNB
time.sleep(20)

approve('0xFFdF4Fe05899C4BdB1676e958FA9F21c19ECB9D5', nft2)  # approve 2nd NFT for LZ
time.sleep(40)

lz_bridge_nft(nft2, 181)  # Отправили из Полигона в Mantle через LZ
time.sleep(20)

approve('0xFFdF4Fe05899C4BdB1676e958FA9F21c19ECB9D5', nft3)  # approve 3rd NFT for LZ
time.sleep(40)

lz_bridge_nft(nft3, 153)  # Отправили из Полигона в Core Dao через LZ
time.sleep(20)

approve('0x2E953a70C37E8CB4553DAe1F5760128237c8820D', nft4)  # approve 4th NFT

bridge_nft(nft4, 114)  # Отправили из Полигона в Combo Testnet

approve('0xFFdF4Fe05899C4BdB1676e958FA9F21c19ECB9D5', nft5)  # approve 5th NFT for LZ
time.sleep(40)

lz_bridge_nft(nft5, 102)  # Отправили из Полигона в BNB через LZ
time.sleep(random.randint(30, 40))

approve('0xFFdF4Fe05899C4BdB1676e958FA9F21c19ECB9D5', nft6)  # approve 6th NFT for LZ
time.sleep(40)
lz_bridge_nft(nft6, 125)  # Отправили из Полигона в CELO через LZ

# Следующий этап - это клейм с тестовых сетей БНБ и Combo - это файл claim.py - но лучше подождать
