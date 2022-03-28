from requests.adapters import HTTPAdapter, Retry
import validator
import requests
import utils
import json

'''
In an attempt to filter out the noise on the blockchain, I'll maintain a list of addresses, 
which could be internal transactions from the LP or anything not initiated by a user.
I'm not segregating per blockchain, since the collision risk is negligible.
'''
block_addresses = [
    "0x0000000000000000000000000000000000000000",
    "0x9c4350f527ff7f96b650ee894ae9103bdfec0432",
    "0x1111111254fb6c44bac0bed2854e76f90643097d"
]

def get_all_holders_from_block(chain_id, lp_address, token_address, start_block=1):
    '''
    Gets wallet addresses and transaction hashes for anyone who interacts with liquidity pool, starting at block number.

    Input params are case insensitive (lp_address and token_address).

    This function will ignore pagination and offset, for reasons below: 
    - Explorer APIs may return >= 600 transactions per call, and it is unlikely that within 1 minute users will buy/sell a token more than 600 times, or 10x per second.
    - Explorer API doesn't enforce page sizes, meaning, the only way to paginate is using block numbers, which can be complex since Ethereum produces blocks at irregular intervals.
    
    Returns error or list. List can be empty.
    '''
    if not validator.is_eth_address(lp_address):
        return error(message="invalid liquidity pool address: " + lp_address)

    if not validator.is_eth_address(token_address):
        return error(message="invalid token address: " + token_address)

    if not validator.is_chain_valid(chain_id):
        return error(message="invalid chain_id: " + str(chain_id))
    
    params = {
        "module": "account",
        "action": "tokentx",
        "address": lp_address,
        "page": 1,
        "startblock": start_block,
        "endblock": 999999999,
        "sort": "asc",
        "apikey": utils.get_random_key(chain_id)
    }

    r = call_with_retry(utils.get_explorer_endpoint(chain_id), params=params)
    
    if not r.ok:
        return error(r)

    response = r.json()

    result = []

    # status = 0 - no transactions found
    # status = 1 - transactions found
    # status = X - error?
    if 'status' in response and response['status'] not in ('0', '1'):
        return error('failed to fetch holder txns: ' + str(response))
    elif 'status' in response and response['status'] == '0':
        return result

    if 'result' in response:
        for item in response['result']:

            if not filter_out_block_addresses(item, token_address):
                continue

            result.append({
                "txn_hash": item['hash'],
                "block": int(item['blockNumber']),
                "from": item["from"],
                "to": item["to"],
                "contract_address": item["contractAddress"],
                "value": int(item["value"]),
                "timestamp": item["timeStamp"],
                "holder": get_holder(item, lp_address)
            })
    return result

def call_with_retry(path, params):
    s = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
    s.mount('https://', HTTPAdapter(max_retries=retries))
    return s.get(path, params=params)

def filter_out_block_addresses(txn, contract_address):
    if 'from' in txn and txn['from'].lower() in block_addresses:
        return False
    if 'to' in txn and txn['to'].lower() in block_addresses:
        return False
    if 'contractAddress' in txn and txn['contractAddress'].lower() != contract_address.lower():
        return False
    return True

def get_holder(txn, lp_address):
    if 'from' in txn and 'to' in txn and lp_address.lower() == txn['from'].lower():
        return txn['to']
    if 'from' in txn and 'to' in txn and lp_address.lower() == txn['to'].lower():
        return txn['from']
    else:
        return None

def error(r):
    return {
        "type": "error",
        "code": r.status_code,
        "content": r.content
    }

def error(message):
    return {
        "type": "error",
        "code": "INVALID_PARAM",
        "content": message
    }
