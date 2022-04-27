from solcx import compile_standard
from jinja2 import Template
import solcx

def compile(name, ticker, supply_type, initial_supply, is_pausable):

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

    #if pausable
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

    # if snapshot, FUTURE FEATURE
    # if args['snapshot']:
    #     raise Exception('Snapshot not implemented. Crashing')

    # if snapshot, FUTURE FEATURE
    # if args['vote']:
    #     raise Exception('Voting not implemented. Crashing')

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

    result = compiled_sol["contracts"]["CustomToken.sol"]["CustomToken"]["evm"]["bytecode"]["object"]

    if initial_supply:
        initial_supply_int = int(initial_supply)
    else:
        initial_supply_int = 0

    result += str(hex(initial_supply_int)[2:]).zfill(64)

    return result