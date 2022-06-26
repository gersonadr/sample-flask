# from web3 import Web3

# bsc = "https://bsc-dataseed.binance.org/"
# # bsc = "https://data-seed-prebsc-1-s1.binance.org:8545/"
# web3 = Web3(Web3.HTTPProvider(bsc))
# print (web3.isConnected())

# account_1 = "0x60ad2Ec0F7Af5145D1FbD8e43B15774d669f816d"
# account_2 = "0x26F235150e2d4b3E8e63b2bd85A21eCC9Ea4a6e0"

# private = ""

# balance = web3.eth.get_balance(account_1)

# balanceEth = web3.fromWei(balance, 'ether')

# print (balanceEth)

# nonce = web3.eth.getTransactionCount(account_1)

# tx = {
#     'nonce': nonce,
#     'to': account_2,
#     'value': web3.toWei(0.1, 'ether'),
#     'gas': 21000, #default
#     'gasPrice': web3.toWei('50', 'gwei')
# }

# signed_tx = web3.eth.account.sign_transaction(tx, private)

# tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

# transaction = web3.toHex(tx_hash)
# txn_obj = web3.eth.get_transaction(transaction)

# print (txn_obj)