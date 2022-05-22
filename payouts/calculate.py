from config.config import PAYOUT_DB, CREATOR_WALLET, DEVELOPER_WALLET, WEB3_PROVIDER_URI
from contracts.ingredients import ingredients_contract
from contracts.pizza import pizza_contract
from contracts.shop import shop_contract, get_balance_in_shop_contract

import requests
import time
from web3 import Web3

def get_all_pizzas(block):
    pizzas_contract = pizza_contract()
    num_pizzas = pizzas_contract.functions.numPizzas().call(block_identifier=block)

    all_pizzas = []
    for pizza_token_id in range(1, num_pizzas+1):
        owner = pizzas_contract.functions.ownerOf(pizza_token_id).call(block_identifier=block)
        if owner == '0x0000000000000000000000000000000000000000':
            continue

        pizza = pizzas_contract.functions.pizza(pizza_token_id).call(block_identifier=block)
        
        all_pizzas.append({
            'token_id': pizza_token_id,
            'data': pizza
        })

    return all_pizzas

def get_all_ingredients(block):
    ingredient_contract = ingredients_contract()
    num_ingredients = ingredient_contract.functions.getNumIngredients().call(block_identifier=block)
    all_ingredients = []
    for ingredient_token_id in range(1, num_ingredients+1):
        ingredient = ingredient_contract.functions.getIngredient(ingredient_token_id).call(block_identifier=block)
        all_ingredients.append({
            'token_id': ingredient_token_id,
            'data': ingredient
        })
    
    return all_ingredients

def pizza_contains_ingredient(pizza, ingredient_token_id):
    if pizza[0] == ingredient_token_id:
        return True
    
    if pizza[1] == ingredient_token_id:
        return True

    for ingredients in pizza[2:]:
        for pizza_ingredient in ingredients:
            if pizza_ingredient == 0:
                break 

            if pizza_ingredient == ingredient_token_id:
                return True 
    return False

def calculate_ingredient_rarities(all_pizzas, all_ingredients):
    rarities = []

    for ingredient in all_ingredients:
        pizzas_with_ingredient = 0

        for pizza in all_pizzas:
            if pizza_contains_ingredient(pizza['data'], ingredient['token_id']):
                pizzas_with_ingredient += 1
        
        rarities.append({
            'ingredient': ingredient,
            'rarity': 100.0 * float(pizzas_with_ingredient) / float(len(all_pizzas))
        })
    
    return rarities

def calculate_pizza_rarities(ingredient_rarities, all_pizzas):
    rarities = []

    for pizza in all_pizzas:
        pizzas_ingredient_rarities = []

        for ingredient_rarity in ingredient_rarities:
            ingredient_type = ingredient_rarity['ingredient']['data'][1]

            if ingredient_type == 0 or ingredient_type == 1: # Base or Sauce
                if not pizza_contains_ingredient(pizza['data'], ingredient_rarity['ingredient']['token_id']):
                    continue

                pizzas_ingredient_rarities.append(ingredient_rarity['rarity'])

            else: # all other ingredients
                if pizza_contains_ingredient(pizza['data'], ingredient_rarity['ingredient']['token_id']):
                    pizzas_ingredient_rarities.append(ingredient_rarity['rarity'])
                else:
                    pizzas_ingredient_rarities.append(100.0 - ingredient_rarity['rarity'])

        rarities.append({
            'pizza': pizza,
            'rarity': round(sum(pizzas_ingredient_rarities) / len(pizzas_ingredient_rarities), 3)
        })
    
    return rarities

def get_unclaimed_payouts(block):
    pizza_shop_contract = shop_contract()
    all_payouts = requests.get(PAYOUT_DB).json()
    
    unclaimed = []
    for address, payout_history in all_payouts.items():
        for payout in payout_history:
            if payout['block'] > block: # don't account for future payouts
                continue

            is_paid_out = pizza_shop_contract.functions.isPaidOutForBlock(address, payout['block']).call(block_identifier=block)

            if not is_paid_out:
                unclaimed.append({
                    'address': address,
                    'payout': payout
                })

    return unclaimed

def get_artist_unclaimed_total(block, all_ingredients):
    pizza_shop_contract = shop_contract()

    unclaimed_total = 0
    artists = {}
    for ingredient in all_ingredients:
        artist = ingredient['data'][2]
        if artist in artists:
            continue

        try:
            allowed_withdrawal_amount = pizza_shop_contract.functions.artistAllowedWithdrawalAmount(artist).call(block_identifier=block)
            unclaimed_total += allowed_withdrawal_amount
            artists[artist] = True

        except:
            continue
        
    return unclaimed_total

def get_owner_of_pizza_token_id(block, token_id):
    pizzas_contract = pizza_contract()
    return pizzas_contract.functions.ownerOf(token_id).call(block_identifier=block)

def calculate_payouts(block):
    # fetch all the pizzas and all the ingredients
    all_pizzas = get_all_pizzas(block)
    all_ingredients = get_all_ingredients(block)

    # calculate rarities
    ingredient_rarities = calculate_ingredient_rarities(all_pizzas, all_ingredients)
    pizza_rarities = calculate_pizza_rarities(ingredient_rarities, all_pizzas)

    # get the rarest pizzas
    rarest_pizzas = [] 
    lowest_rarity = None
    for pizza_rarity in pizza_rarities:
        if lowest_rarity == None:
            rarest_pizzas.append(pizza_rarity['pizza'])
            lowest_rarity = pizza_rarity['rarity']
            continue
        
        if pizza_rarity['rarity'] == lowest_rarity:
            rarest_pizzas.append(pizza_rarity['pizza'])
            continue 

        if pizza_rarity['rarity'] < lowest_rarity:
            rarest_pizzas = [pizza_rarity['pizza']]
            lowest_rarity = pizza_rarity['rarity']

    # calculate the prize pool
    total_balance = get_balance_in_shop_contract(block)

    unclaimed_payouts = get_unclaimed_payouts(block)
    unclaimed_payouts_total = 0
    for payout in unclaimed_payouts:
        unclaimed_payouts_total += payout['payout']['payout_amount'] * 1000000000000000000

    artist_unclaimed_total = get_artist_unclaimed_total(block, all_ingredients)

    prize_pool = total_balance - unclaimed_payouts_total - artist_unclaimed_total
    developer_rewards = prize_pool * 0.0025
    creator_rewards = prize_pool * 0.0075
    rarity_rewards = prize_pool * 0.01
    
    # determine which address's are getting rewarded from the rarity rewards
    rarity_rewarded_owners = []
    for pizza in rarest_pizzas:
        address = get_owner_of_pizza_token_id(block, pizza['token_id'])
        token_id = pizza['token_id']
        rarity_rewarded_owners.append((address, token_id))

    # get the timestamp for this block
    timestamp = None
    try:
        w3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER_URI))
        block_obj = w3.eth.get_block(block_identifier=block)
        timestamp = block_obj['timestamp']
    except:
        timestamp = int(time.time()) 

    payouts = [
        {
            'address': CREATOR_WALLET,
            'payout_amount': int(creator_rewards),
            'reason': 'Creator',
            'timestamp': timestamp
        },
        {
            'address': DEVELOPER_WALLET,
            'payout_amount': int(developer_rewards),
            'reason': 'Developer',
            'timestamp': timestamp
        }
    ]

    for (address, token_id) in rarity_rewarded_owners:
        payouts.append({
            'address': address,
            'payout_amount': int(rarity_rewards / float(len(rarity_rewarded_owners))),
            'reason': 'Rarity reward',
            'timestamp': timestamp,
            'token_id': token_id,
            'rarity': lowest_rarity
        })

    return payouts
