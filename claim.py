import json
from web3 import Web3
import time
import random
import requests
from fake_useragent import UserAgent
from conf import *

opBNB = 'https://opbnb-testnet-rpc.bnbchain.org'
Combo = 'https://test-rpc.combonetwork.io'

Combo_explorer = 'https://combotrace-testnet.nodereal.io/tx/'
opBNB_explorer = 'https://opbnbscan.com/tx/'

opBNB_bridge_add = '0x4CC870C8fDfBC512943FE60c29c98d515f868EBF'
Combo_bridge_add = '0x2eD78A532C2BfdB8D739F1f27BAD87D5e27CCCd1'

ua = UserAgent()

w3 = Web3(Web3.HTTPProvider('https://polygon-rpc.com/'))
account = w3.eth.account.from_key(PRIVATE)
address = account.address

print(time.strftime("%H:%M:%S", time.localtime()))
print(f'{address}', flush=True)


def claim_nft(PRIVATE, tx_hash, chain, chainId, explorer_link, bridge_address):
    headers = {
        'authority': 'api.zkbridge.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en,ru;q=0.9,fr;q=0.8,ru-RU;q=0.7,en-US;q=0.6',
        'content-type': 'application/json',
        'origin': 'https://zkbridge.com',
        'referer': 'https://zkbridge.com/',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': ua.random,
    }

    json_data = {
        'tx_hash': tx_hash.strip(),
        'chain_id': 4,
    }

    response = requests.post(
        'https://api.zkbridge.com/api/v2/receipt_proof/generate',
        headers=headers,
        json=json_data,
    )

    srcChainId = json.loads(response.text)['chain_id']
    srcBlockHash = json.loads(response.text)['block_hash']
    logIndex = json.loads(response.text)['proof_index']
    mptProof = json.loads(response.text)['proof_blob']

    ww3 = Web3(Web3.HTTPProvider(chain))

    account = ww3.eth.account.from_key(PRIVATE)
    address = account.address

    print(time.strftime("%H:%M:%S", time.localtime()))
    print(f'{address}', flush=True)

    abi_validate = json.load(open('validate_abi.json'))
    bridge_add = ww3.to_checksum_address(bridge_address)
    br_contract = ww3.eth.contract(address=bridge_add, abi=abi_validate)

    try:
        nonce = ww3.eth.get_transaction_count(address)
        txn = br_contract.functions.validateTransactionProof(srcChainId, srcBlockHash, logIndex, mptProof
                                                             ).build_transaction({
            'from': address,
            'gasPrice': ww3.eth.gas_price,
            'chainId': chainId,
            'nonce': nonce,
        })
        gasLimit = ww3.eth.estimate_gas(txn)
        txn['gas'] = int(gasLimit * 1.3)
        signed_txn = ww3.eth.account.sign_transaction(txn, PRIVATE)
        txn_hash = ww3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print(f"NFT Claimed {explorer_link}{txn_hash.hex()}")

    except Exception as err:
        print(f"Unexpected {err=}")


with open(f'{address}_hashes.txt', 'r') as h:
    hash1 = h.readline()  # Hash от бриджа в opBNB
    hash2 = h.readline()  # Hash от бриджа в Combo Network

# Начинаем клейм НФТ - сначала в opBNB через 30 секунд Combo

claim_nft(PRIVATE, hash1, opBNB, 5611, opBNB_explorer, opBNB_bridge_add)
time.sleep(random.randint(20, 30))
claim_nft(PRIVATE, hash2, Combo, 91715, Combo_explorer, Combo_bridge_add)
