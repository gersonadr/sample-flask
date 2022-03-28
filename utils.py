import validator
import random

def get_explorer_endpoint(chain_id):
    
    if not validator.is_chain_valid(chain_id):
        return error("invalid chain id:" + str(chain_id))

    chain_urls = {
        1: "https://api.etherscan.io/api",
        3: "https://api-ropsten.etherscan.io/api",
        4: "https://api-rinkeby.etherscan.io/api",
        5: "https://api-goerli.etherscan.io/api",
        42: "https://api-kovan.etherscan.io/api",
        56: "https://api.bscscan.com/api",
        97: "https://api-testnet.bscscan.com/api",
        137: "https://api.polygonscan.com/api",
        80001: "https://api-testnet.polygonscan.com/"
    }

    chain_id_numeric = int(chain_id)

    return chain_urls[chain_id_numeric]

def get_random_key(chain_id):

    if not validator.is_chain_valid(chain_id):
        return error("invalid chain id:" + str(chain_id))

    # mainnet keys work on testnets
    if chain_id in (3, 4, 5, 42):
        chain_id = 1
    elif chain_id == 97:
        chain_id = 56
    elif chain_id == 80001:
        chain_id = 137

    keys = {
        1: [
            "S46JREZEKRV6PXR17C16GTRK2QVFBEEZ1D"
        ],
        56: [
            "V1SXBSXMIG95CKUZST79DRCD2NIFSFY279"
        ],
        137: [
            "J7APK7P6QCB7EWCTA3FWA8DIG8PXWZFMX3"
        ]
    }

    return random.choice(keys[chain_id])
    
def error(message):
    return {
        "type": "error",
        "code": "CHAIN_ID",
        "content": message
    }