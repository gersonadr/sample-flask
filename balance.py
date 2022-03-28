from requests.adapters import HTTPAdapter, Retry
import validator
import requests
import utils

def get_holder_balance(chain_id, token_address, wallet_address):
    '''
    Get balance in token units for a single wallet.
    Will resolve endpoint to call based on chain_id.
    Will retry up to 5 times.
    '''
    if not validator.is_eth_address(token_address):
        return error(message="invalid token address: " + token_address)

    if not validator.is_eth_address(wallet_address):
        return error(message="invalid wallet address: " + wallet_address)

    if not validator.is_chain_valid(chain_id):
        return error(message="invalid chain_id: " + str(chain_id))

    params = {
        "module": "account",
        "action": "tokenbalance",
        "contractaddress": token_address,
        "address": wallet_address,
        "page": 1,
        "startblock": 0,
        "endblock": 999999999,
        "sort": "asc",
        "apikey": utils.get_random_key(chain_id)
    }

    r = call_with_retry(utils.get_explorer_endpoint(chain_id), params=params)
    
    if r.ok:
        return r.json()
    else:
        return error(r)

def call_with_retry(path, params):
    s = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
    s.mount('https://', HTTPAdapter(max_retries=retries))
    return s.get(path, params=params)

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

