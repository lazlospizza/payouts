import json
from web3 import Web3

from config.config import SHOP_CONTRACT_ADDRESS, WEB3_PROVIDER_URI

def shop_contract():
    w3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER_URI))

    with open("./abi/LazlosPizzaShop.json") as f:
        info_json = json.load(f)
        abi = info_json['abi']
        address = Web3.toChecksumAddress(SHOP_CONTRACT_ADDRESS)
        return w3.eth.contract(address=address, abi=abi)



def get_balance_in_shop_contract(block):
    w3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER_URI))
    address = Web3.toChecksumAddress(SHOP_CONTRACT_ADDRESS)
    return w3.eth.getBalance(address, block_identifier=block)