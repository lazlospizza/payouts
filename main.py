from config.config import BLOCK
from payouts.calculate import calculate_payouts

if __name__ == '__main__':
    print('\n--------------- Calculating Payouts ----------------')
    print(f'Block: {BLOCK}\n')

    payouts = calculate_payouts(int(BLOCK))
    for (i, payout) in enumerate(payouts):
        print(f'{payout["reason"]}')
        print(f'Address: {payout["address"]}')
        print(f'Amount: {payout["payout_amount"]}\n')

    print('----------------------------------------------------\n')
