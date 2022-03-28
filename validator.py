import re

def is_eth_address(address):
    if address:
        pattern = re.compile("^0x[a-fA-F0-9]{40}$")
        return pattern.match(address)
    return False

def is_chain_valid(chain_id):

    if not chain_id:
        return False

    try:
        chain_numeric = int(chain_id)
    except ValueError:
        return False

    return chain_numeric in [
        1, #Ethereum 
        3, #Ropsten
        4, #Rinkeby
        5, #Goerli
        42, #Kovan
        56, #Binance
        97, #Binance Testnet
        137, #Polygon
        80001 #Polygon Mumbai Testnet
        ]