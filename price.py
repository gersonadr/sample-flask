from requests.adapters import HTTPAdapter, Retry
import requests
import validator

def get_price(chain_id, ref_token, my_token):
    if not validator.is_eth_address(ref_token):
        return error(message="invalid ref_token address: " + ref_token)

    if not validator.is_eth_address(my_token):
        return error(message="invalid my_token address: " + my_token)

    if not validator.is_chain_valid(chain_id):
        return error(message="invalid chain_id: " + str(chain_id))

    params = {
        "fromTokenAddress": ref_token,
        "toTokenAddress": my_token,
        "amount": 1
    }

    r = call_with_retry(f"https://api.1inch.io/v4.0/{chain_id}/quote", params=params)
    
    if r.ok:
        response = r.json()
        return '{:.20f}'.format(1 / float(response["toTokenAmount"]))

    else:
        return error(r)

def get_ETH_price():

    params = {
        "fromTokenAddress": "0x2170ed0880ac9a755fd29b2688956bd959f933f8",
        "toTokenAddress": "0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d",
        "amount": 1000000000000000000,
        "slippage": 0
    }

    r = call_with_retry(f"https://api.1inch.io/v4.0/56/quote", params=params)
    if r.ok:
        response = r.json()
        return float(response["toTokenAmount"]) / 10**18

    else:
        return error(r)

def get_BNB_price():

    params = {
        "fromTokenAddress": "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c",
        "toTokenAddress": "0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d",
        "amount": 1000000000000000000,
        "slippage": 0
    }

    r = call_with_retry(f"https://api.1inch.io/v4.0/56/quote", params=params)
    if r.ok:
        response = r.json()
        return float(response["toTokenAmount"])/10**18

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
        "code": "ADDR_INVALID",
        "content": message
    }

