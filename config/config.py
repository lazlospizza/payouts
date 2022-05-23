import os

INGREDIENTS_CONTRACT_ADDRESS = '0xd2e5992ce910b2ab7921f653de827b2e5d5ae828'
PIZZA_CONTRACT_ADDRESS = '0x652aa63f0349c296e5082dc1fd62aeb91b2c419a'
SHOP_CONTRACT_ADDRESS = '0x93d6e1b962606470c5c28fdb56dcf53b1bb1cd8c'

CREATOR_WALLET = '0x81A5e6fDA965b67A8a4D097073Edba09331073a4'
DEVELOPER_WALLET = '0x7701FEFd637eB85E2d7d5495b3C3b33703B8e847'

PAYOUT_DB = 'https://lazlos-pizza.s3.amazonaws.com/payouts/mainnet.json'

BLOCK = os.getenv('BLOCK')
if BLOCK == None:
    raise Exception('BLOCK is required')

WEB3_PROVIDER_URI = os.getenv('WEB3_PROVIDER_URI')
if WEB3_PROVIDER_URI == None:
    raise Exception('WEB3_PROVIDER_URI required')

UPLOAD_TO_S3 = os.getenv("UPLOAD_TO_S3") == "true"
