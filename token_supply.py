from requests.adapters import HTTPAdapter, Retry
import validator
import requests
import utils

def get_max_supply(chain_id, token_address):
    if not validator.is_eth_address(token_address):
        return error(message="invalid token address: " + token_address)

    if not validator.is_chain_valid(chain_id):
        return error(message="invalid chain_id: " + str(chain_id))

    params = {
        "module": "stats",
        "action": "tokensupply",
        "contractaddress": token_address,
        "page": 1,
        "startblock": 0,
        "endblock": 999999999,
        "sort": "asc",
        "apikey": utils.get_random_key(chain_id)
    }

    r = call_with_retry(utils.get_explorer_endpoint(chain_id), params=params)
    
    if not r.ok:
        return error(r)
    
    result = r.json()

    if 'status' in result and result['status'] == '1':
        max_supply = int(result['result'])
        if not max_supply:
            return error('token not found: ' + token_address)
        else:
            return int(result['result'])
    else:
        return error('unable to fetch max supply for token ' + token_address + ': ' + str(result))
    
def call_with_retry(path, params):
    s = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
    s.mount('https://', HTTPAdapter(max_retries=retries))
    return s.get(path, params=params)

def error(message):
    return {
        "type": "error",
        "code": "INVALID_PARAM",
        "content": message
    }