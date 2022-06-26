from web3 import Web3
import os

def transfer_bnb(to_account, value):

    # bsc = "https://bsc-dataseed.binance.org/"
    # bsc = "https://data-seed-prebsc-1-s1.binance.org:8545/"
    
    bsc_endpoint = os.getenv("BNB_ENDPOINT")
    web3 = Web3(Web3.HTTPProvider(bsc_endpoint))
    print (web3.isConnected())

    from_account = os.getenv("BNB_WALLET")

    private = os.getenv("PRIVATE_KEY")

    # balance = web3.eth.get_balance(from_account)
    # balanceEth = web3.fromWei(balance, 'ether')
    # print (balanceEth)

    nonce = web3.eth.getTransactionCount(from_account)

    tx = {
        'nonce': nonce,
        'to': to_account,
        'value': web3.toWei(value, 'ether'),
        'gas': 21000, #default
        'gasPrice': web3.toWei('50', 'gwei')
    }

    signed_tx = web3.eth.account.sign_transaction(tx, private)

    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

    transaction = web3.toHex(tx_hash)

    return transaction