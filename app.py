
from flask import Flask, request
from flask import render_template
from urllib.parse import unquote
import compiler
import transfer
import holder
import price
import balance
import blockchain
import gasestimator
import json

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")

#DEPRECATED - This uses 1inch REST API. Use /swap instead
@app.route("/price/<chain_id>/<ref_token>/<my_token>")
def get_price(chain_id, ref_token, my_token):
    return json.dumps(price.get_price(chain_id, ref_token, my_token))

@app.route("/swap/<chain_id>/<ref_token>/<my_token>")
def get_swap(chain_id, ref_token, my_token):
    return str(blockchain.get_swap(chain_id, ref_token, my_token))

@app.route("/holder/<chain_id>/<lp_address>/<token_address>/<start_block>")
def get_holder(chain_id, lp_address, token_address, start_block):
    return json.dumps(holder.get_all_holders_from_block(int(chain_id), lp_address, token_address, int(start_block)))

@app.route("/balance/<chain_id>/<token_address>/<wallet_address>")
def get_balance(chain_id, token_address, wallet_address):
    return json.dumps(balance.get_holder_balance(int(chain_id), token_address, wallet_address))

# @app.route("/price/<contract_address>")
# def compile_sol(initial_supply):

#     contract_file = "./contracts/OurToken.sol"
#     return compiler.compile(contract_file, initial_supply)

@app.route("/price/ETH/USD")
def get_ETH_price():
    return str(price.get_ETH_price())

@app.route("/price/BNB/USD")
def get_BNB_price():
    return str(price.get_BNB_price())

# @app.route("/env/<name>")
# def get_env_variable(name):
#     return os.getenv(name)

# @app.route("/transfer/bnb/<to_account>/<value>")
# def transfer_bnb(to_account, value):
#     return transfer.transfer_bnb(to_account, value)

@app.route("/compile/<name>/<ticker>/<supply_type>/<initial_supply>/<is_pausable>")
def compile_sol(name, ticker, supply_type, initial_supply, is_pausable):

    if is_pausable == "false":
        is_pausable = False
    else:
        is_pausable = True

    initial_supply = int(initial_supply) * 10**6

    return compiler.compile(unquote(name), unquote(ticker), supply_type, initial_supply, is_pausable)

@app.route("/estimate/<chain_id>/<name>/<ticker>/<supply_type>/<is_pausable>/<has_transfer>")
def estimate_gas_create_contract(chain_id, name, ticker, supply_type, is_pausable, has_transfer):

    if is_pausable == "false":
        is_pausable = False
    else:
        is_pausable = True

    gas_estimate = float(gasestimator.estimate_gas_create_contract(chain_id, name, ticker, supply_type, is_pausable))
    
    if has_transfer:
        gas_estimate += float(gasestimator.estimate_gas_transfer(chain_id))

    if chain_id == 1 or chain_id == 42:
        onramp_fees = 0.002
    else:
        onramp_fees = 0.011
        
    gas_estimate += onramp_fees

    return str(gas_estimate)