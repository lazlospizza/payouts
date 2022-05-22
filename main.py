from config.config import BLOCK, UPLOAD_TO_S3
from payouts.calculate import calculate_payouts
from s3.s3 import upload_to_s3

if __name__ == '__main__':
    print('\n--------------- Calculating Payouts ----------------')
    print(f'Block: {BLOCK}\n')

    payouts = calculate_payouts(int(BLOCK))
    for (i, payout) in enumerate(payouts):
        print(f'{payout["reason"]}')
        print(f'Address: {payout["address"]}')

        if 'token_id' in payout:
            print(f'Token ID: {payout["token_id"]}')
            print(f'Rarity: {payout["rarity"]}')

        print(f'Amount: {payout["payout_amount"]}\n')

    print('----------------------------------------------------\n')

    if UPLOAD_TO_S3:
        upload_to_s3(int(BLOCK), payouts)
