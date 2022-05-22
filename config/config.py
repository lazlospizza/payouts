import os

INGREDIENTS_CONTRACT_ADDRESS = '0x1F68C55Cf9A7B458E73906347cAe6d8cA2236e79'
PIZZA_CONTRACT_ADDRESS = '0x45Fa7B1fB74011D6258d388fD665B1f55E73464f'
SHOP_CONTRACT_ADDRESS = '0x80B39de84D97C98bD1D58717502dBB5253885682'

CREATOR_WALLET = '0x81A5e6fDA965b67A8a4D097073Edba09331073a4'
DEVELOPER_WALLET = '0x7701FEFd637eB85E2d7d5495b3C3b33703B8e847'

PAYOUT_DB = 'https://lazlos-pizza.s3.amazonaws.com/payouts/rinkeby.json'

BLOCK = os.getenv('BLOCK')
if BLOCK == None:
    raise Exception('BLOCK is required')

WEB3_PROVIDER_URI = os.getenv('WEB3_PROVIDER_URI')
if WEB3_PROVIDER_URI == None:
    raise Exception('WEB3_PROVIDER_URI required')
