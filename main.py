from config.config import BLOCK
from payouts.calculate import calculate_payouts
from s3.s3 import upload_to_s3

if __name__ == '__main__':
    print('\n--------------- Calculating Payouts ----------------')
    print(f'Block: {BLOCK}\n')

    payouts = calculate_payouts(int(BLOCK))
    for (i, payout) in enumerate(payouts):
        print(f'{payout["reason"]}')
        print(f'Address: {payout["address"]}')
        print(f'Amount: {payout["payout_amount"]}\n')

    print('----------------------------------------------------\n')

    upload_to_s3(int(BLOCK), payouts)