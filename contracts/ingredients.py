import json
from web3 import Web3

from config.config import INGREDIENTS_CONTRACT_ADDRESS, WEB3_PROVIDER_URI

def ingredients_contract():
    w3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER_URI))

    with open("./abi/LazlosIngredients.json") as f:
        info_json = json.load(f)
        abi = info_json['abi']
        address = Web3.toChecksumAddress(INGREDIENTS_CONTRACT_ADDRESS)
        return w3.eth.contract(address=address, abi=abi)

