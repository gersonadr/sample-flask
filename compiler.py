# from solcx import compile_standard
# import solcx

# def compile(contract_file, initial_supply):

#     solcx.install_solc("0.8.0")

#     with open(contract_file, "r") as file:
#         our_token = file.read()

#     compiled_sol = compile_standard(
#         {
#             "language": "Solidity",
#             "sources": {"OurToken.sol": {"content": our_token}},
#             "settings": {
#                 "outputSelection": {
#                     "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
#                 }
#             },
#         },
#         solc_version="0.8.0",
#     )

#     result = compiled_sol["contracts"]["OurToken.sol"]["BEP20NoDependencies"]["evm"]["bytecode"]["object"]

#     if not initial_supply:
#         initialSupplyInt = 1000000000000000000000000
#     else:
#         initialSupplyInt = int(initial_supply)

#     result += str(hex(initialSupplyInt)[2:]).zfill(64)
#     return result