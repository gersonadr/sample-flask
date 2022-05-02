from web3 import Web3
import utils
import json

with open('contracts/Router-abi.json') as f:
    router_abi = json.load(f)

def get_swap(chain_id, address_from, address_to):

    endpoint = utils.get_rpc_endpoint(chain_id)

    w3 = Web3(Web3.HTTPProvider(endpoint))

    router_address = utils.get_router_address(chain_id)

    router_instance = w3.eth.contract(address=router_address, abi=router_abi)

    swap_rate = router_instance.functions.getAmountsOut(1000, [address_from, address_to]).call()

    if swap_rate and len(swap_rate) == 2:
        return float(swap_rate[0]) / float(swap_rate[1])

    return swap_rate

# print (get_swap(97, '0x71E0C6DD765b990C8F53DaF753AB36064C481670', '0xC94B3ba0dD04726CF294CdC5f7BE973742eF989C'))