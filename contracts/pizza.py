import json
from web3 import Web3

from config.config import PIZZA_CONTRACT_ADDRESS, WEB3_PROVIDER_URI

def pizza_contract():
    w3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER_URI))

    with open("./abi/LazlosPizza.json") as f:
        info_json = json.load(f)
        abi = info_json['abi']
        address = Web3.toChecksumAddress(PIZZA_CONTRACT_ADDRESS)
        return w3.eth.contract(address=address, abi=abi)
