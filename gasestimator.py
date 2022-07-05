from solcx import compile_standard
from jinja2 import Template
from web3 import Web3
import solcx
import utils
import json
import os

def estimate_gas_create_contract(chain_id, name, ticker, supply_type, is_pausable):

    solcx.install_solc("0.8.0")
    C_CONTRACTS_HOME = './contracts/'

    with open(C_CONTRACTS_HOME + 'CustomToken.sol', 'r') as file:
        template_file = file.read()

    # always loads ERC20 since it applies to all tokens
    with open(C_CONTRACTS_HOME + 'ERC20.sol', 'r') as file:
        erc20 = file.read()

    methods = ''
    extends = 'ERC20'

    # if token is variable, enable Mintable & Burnable
    if supply_type == 'variable':
        with open(C_CONTRACTS_HOME + 'Mintable.sol', 'r') as file:
            import_mintable = file.read()

        methods += """
        function mint(address to, uint256 amount) public onlyOwner {
            _mint(to, amount);
        }
        """

        extends += ', ERC20Burnable, Ownable'
    else:
        import_mintable = ""

    if is_pausable:
        with open(C_CONTRACTS_HOME + 'Pausable.sol', 'r') as file:
            import_pausable = file.read()

        methods += """

        function pause() public onlyOwner {
            _pause();
        }

        function unpause() public onlyOwner {
            _unpause();
        }

        function _beforeTokenTransfer(address from, address to, uint256 amount)
            internal
            whenNotPaused
            override
        {
            super._beforeTokenTransfer(from, to, amount);
        }

        """

        extends += ', Pausable'
    else:
        import_pausable = ""

    data = {
        "name": name,
        "ticker": ticker,
        "import_ERC20": erc20,
        "import_mintable": import_mintable,
        "import_pausable": import_pausable,
        "extends": extends,
        "methods": methods
    }

    j2_template = Template(template_file)
    contract = j2_template.render(data)

    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {"CustomToken.sol": {"content": contract}},
            "settings": {
                "outputSelection": {
                    "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
                }
            },
        },
        solc_version="0.8.0",
    )

    bytecode = compiled_sol["contracts"]["CustomToken.sol"]["CustomToken"]["evm"]["bytecode"]["object"]

    abi = json.loads(compiled_sol["contracts"]["CustomToken.sol"]["CustomToken"]["metadata"])["output"]["abi"]

    w3 = Web3(Web3.HTTPProvider(utils.get_rpc_endpoint(chain_id)))

    my_address = '0xF9F123D8b2C8202393a982eEf2228cC899d5556b' #any wallet will do

    bytecode += str(hex(1000)[2:]).zfill(64)

    transaction = {
        "data": bytecode,
        "from": my_address,
        "value": "0x0",
    }

    txn_gas = w3.eth.estimate_gas(transaction)

    # print ('gas price ' + str(w3.eth.gasPrice))
    # print ('contract gas ' + str(txn_gas))
    # print ('contact gas * gas price * 1.5 ' + str(w3.fromWei(txn_gas * w3.eth.gasPrice * 1.5, 'ether')))

    return w3.fromWei(txn_gas * w3.eth.gasPrice * 2, 'ether')

def estimate_gas_transfer(chain_id):
    try:
        w3 = Web3(Web3.HTTPProvider(utils.get_rpc_endpoint(chain_id)))

        from_wallet = "0x102006244eD480DFD390fC0a32Ae3bC9E057E75f"

        nonce = w3.eth.getTransactionCount(from_wallet)

        to_wallet = "0xa6f79B60359f141df90A0C745125B131cAAfFD12" #any wallet will do

        gas_estimate = w3.eth.estimateGas({
            "from": from_wallet,       
            "nonce": nonce, 
            "to": to_wallet,     
            "value": 1 * 10**18
        })
        
        return w3.fromWei(gas_estimate * w3.eth.gasPrice * 2, 'ether')

    except Exception as e:
        return 0
