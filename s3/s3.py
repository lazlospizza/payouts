from aiohttp import ClientError
from config.config import PAYOUT_DB

import boto3
import json
import requests

def upload_to_s3(block, payouts):
    payouts_db = requests.get(PAYOUT_DB).json()
    
    for payout in payouts:
        entry = {
            'block': block,
            'payout_amount': float(payout['payout_amount']) / float(1000000000000000000),
            'token_id': payout['token_id'] if 'token_id' in payout else None,
            'timestamp': payout['timestamp']
        }

        if payout['address'] not in payouts_db:
            payouts_db[payout['address']] = [entry]

        else:
            payouts_db[payout['address']].append(entry)

    try:
        s3 = boto3.resource('s3')
        object = s3.Object('lazlos-pizza', 'payouts/mainnet.json')
        object.put(Body=bytes(json.dumps(payouts_db).encode('UTF-8')), ContentType='application/json')

    except Exception as e:
        print(f'Failed to upload to S3: {e}')
        return

    print('Successfully updated payout db in S3.')
    return
