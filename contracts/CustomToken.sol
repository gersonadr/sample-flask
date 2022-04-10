{{ import_ERC20 }}
{{ import_mintable }}
{{ import_pausable }}

contract CustomToken is {{ extends }} {
    constructor(uint256 initialSupply, string memory name, string memory ticker) ERC20(name, ticker) {
        _mint(msg.sender, initialSupply * 10 ** decimals());
    }

    {{ methods }}
}