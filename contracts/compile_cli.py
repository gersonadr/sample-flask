from solcx import compile_standard
from jinja2 import Template
import argparse
import solcx

# python compile_cli.py --supply variable --pausable True

parser = argparse.ArgumentParser()
parser.add_argument("--name", help="Token name")
parser.add_argument("--ticker", help="Token ticker")
parser.add_argument("--initial_supply", help="Amount of tokens to pre-mint")
parser.add_argument("--supply", help="Indicates the token supply is fixed or variable")
parser.add_argument("--pausable", help="Indicates the token can be paused by owner")
parser.add_argument("--snapshot", help="Indicates the owner can take a snapshot of holders on-chain")
parser.add_argument("--vote", help="Indicates the token has governance")
args = vars(parser.parse_args())

with open('CustomToken.sol', 'r') as file:
    template_file = file.read()

# always loads ERC20 since it applies to all tokens
with open('ERC20.sol', 'r') as file:
    erc20 = file.read()

methods = ''
extends = 'ERC20'

# if token is variable, enable Mintable & Burnable
if args['supply'] == 'variable':
    with open('Mintable.sol', 'r') as file:
        import_mintable = file.read()

    methods += """

    function mint(address to, uint256 amount) public onlyOwner {
        _mint(to, amount);
    }
    
    """

    extends += ', ERC20Burnable, Ownable'
else:
    import_mintable = ""

#if pausable
if args['pausable']:
    with open('Pausable.sol', 'r') as file:
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

# if snapshot, FUTURE FEATURE
if args['snapshot']:
    raise Exception('Snapshot not implemented. Crashing')

# if snapshot, FUTURE FEATURE
if args['vote']:
    raise Exception('Voting not implemented. Crashing')

data = {
    "name": args['name'],
    "ticker": args['ticker'],
    "import_ERC20": erc20,
    "import_mintable": import_mintable,
    "import_pausable": import_pausable,
    "extends": extends,
    "methods": methods
}

j2_template = Template(template_file)
contract = j2_template.render(data)

solcx.install_solc("0.8.0")

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

result = compiled_sol["contracts"]["CustomToken.sol"]["CustomToken"]["evm"]["bytecode"]["object"]

if args['initial_supply']:
    initial_supply_int = int(args['initial_supply'])
else:
    initial_supply_int = 0

result += str(hex(initial_supply_int)[2:]).zfill(64)

print (result)